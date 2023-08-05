#!/usr/bin/env python3

import re
import os
import sys
import shutil
import string
import base64
import secrets
import inspect
import subprocess
from pathlib import Path
from functools import lru_cache, cached_property

import yaml
import click
try:
    from cryptography.fernet import Fernet, InvalidToken
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
    cryptography_support = True
except:
    class InvalidToken(NotImplementedError):
        pass
    cryptography_support = False
try:
    import gnupg
    env = os.environ
    try:
        if tty_name := os.ttyname(sys.stdin.fileno()):
            env['GPG_TTY'] = tty_name
    except:
        pass
    _gpg = gnupg.GPG(use_agent=True, env=env)
except:
    _gpg = None

from . import git

DEFAULT_FILE_NAME = '.hardcoded.yml'
CONFIG_HOME = Path(os.environ.get('XDG_CONFIG_HOME', Path.home()/'.config'))
DEFAULT_FILE_PATH = CONFIG_HOME / DEFAULT_FILE_NAME.strip('.')
NOT_GIVEN = object()

class _DataFile:
    def __init__(self, path):
        self.path = path
        self._explicitly_not_encrypted = dict()


    def get(self, key, default=None):
        return self.data.get(key, default)


    def set(self, key, value):
        data = self.data
        data[key] = value
        self.data = data


    @property
    def data(self):
        try:
            with open(self.path, 'r') as f:
                data = yaml.safe_load(f) or dict()
                self._explicitly_not_encrypted = dict()
                if set(data.keys()) > set(('salt', 'encrypted')):
                    for k, v in data.items():
                        if k not in ('salt', 'encrypted'):
                            self._explicitly_not_encrypted[k] = v
                return data
        except FileNotFoundError as ex:
            return dict()


    @data.setter
    def data(self, data):
        if set(data.keys()) >= set(('salt', 'encrypted')):
            data.update(self._explicitly_not_encrypted)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.path, 'w') as f:
            yaml.safe_dump(data, f)


class _OneLayerDeeper:
    def __init__(self):
        self._salt = None
        self._fernet = None
        self._saved_gpg_recipient = None
        self._wrong_password = False
        self.path = None
        self._datafile = None
        self._namespace = None
        self.secret = None
        self.ask_if_not_found = None


    def _get_all_decrypted_data(self):
        data = self._datafile.data
        data_was_decrypted = False
        # Decrypt data if necessary.
        if set(data.keys()) >= set(('salt', 'encrypted')):
            self._salt = base64.urlsafe_b64decode(data.get('salt'))
            ciphertext = data.get('encrypted').encode()
            success = False
            for _ in range(3):
                try:
                    data = yaml.safe_load(self.decrypt(ciphertext)) or dict()
                    success = True
                    break
                except ImportError as ex:
                    raise ex
                except click.Abort:
                    exit(1)
                except InvalidToken as ex:
                    if exception_msg := str(ex):
                        exception_msg = f' ({exception_msg})'
                    click.echo(f'Error while decrypting data file. {exception_msg} Did you enter the correct password?', err=True)
                    self._fernet = None
                    self._wrong_password = True
            if not success:
                raise RuntimeError(f'Unable to successfully decrypt datafile {self.path}.')
            data_was_decrypted = True
        elif data and self.secret:
            # Data should be secret, but was just read without decryption. Write back to force applying encryption.
            self._set_all_data(data)

        if self.secret == None:
            # No secret preference was given. Set based on previous status.
            self.secret = data_was_decrypted

        return data


    @property
    def data(self):
        all_data = self._get_all_decrypted_data() or dict()
        namespace_data = all_data.get(self._namespace, dict())
        return namespace_data


    @data.setter
    def data(self, namespace_data):
        all_data = self._get_all_decrypted_data() or dict()
        all_data[self._namespace] = namespace_data
        self._set_all_data(all_data)


    @property
    def _warned_about_gitignore(self):
        return self._datafile.get('warned_about_gitignore', False)
    @_warned_about_gitignore.setter
    def _warned_about_gitignore(self, value):
        self._datafile.set('warned_about_gitignore', value)


    def _set_all_data(self, data):
        # Format data human readable.
        if self.secret:
            # Encrypt data, format ciphertext and salt human readable again.
            data_bytes = yaml.safe_dump(data).encode()
            data = {
                'salt': base64.urlsafe_b64encode(self.salt).decode(),
                'encrypted': self.encrypt(data_bytes),
                }

        # Save data to file.
        self._datafile.data = data
        
        if self.secret and not self._warned_about_gitignore:
            # Check if file is protected against leaking via git.
            data_file_path = Path(self.path).resolve()
            data_file_name = data_file_path.name
            git_repo_root = git.find_repo_path(data_file_path)
            gitignore_path = git.find_gitignore_path(data_file_path)
            datafile_matched_by_gitignore_rule = git.is_file_matched_by_gitignore_rule(data_file_path)
            if datafile_matched_by_gitignore_rule == False:
                if gitignore_path.exists():
                    # Our data file path did not match any .gitignore rule.
                    question = f'Data file {data_file_path} is not matched by any of the rules in {gitignore_path}. Do you want to add the rule "{data_file_name}"?'
                else:
                    # No .gitignore found in the repo.
                    question = f'{git_repo_root} seems to be a git repository, but there is no .gitignore file protecting data file {data_file_path}. Do you want to create a .gitignore file protecting "{data_file_name}"?'
                if click.confirm(f'WARNING: {question}', default=True, err=True):
                    git.add_gitignore_rule(git_repo_root, data_file_name)
                    click.edit(filename=gitignore_path)
                self._warned_about_gitignore = True


    @property
    def salt(self):
        if not self._salt:
            self._salt = os.urandom(16)
        return self._salt


    def generate_random_password(self):
        minimum_length = 32
        alphabet = string.digits + string.ascii_letters + '-_.,'
        while True:
            password = ''.join(secrets.choice(alphabet) for i in range(minimum_length)).strip()
            # TODO: Combine this with the current check on manually entered passwords.
            if (any(c.islower() for c in password)
                    and any(c.isupper() for c in password)
                    and sum(c.isdigit() for c in password) >= 3
                    and len(password) >= minimum_length):
                return password


    def get_password(self):
        account = str(Path(self.path).resolve())
        password = None
        
        # Try the Apple Keychain.
        save_to_keychain = False
        if (not password) and shutil.which('security'):
            save_to_keychain = True
            if not self._wrong_password:
                try:
                    completed_process = subprocess.run(['security', 'find-internet-password', '-a', account, '-s', 'hardcoded', '-w'], capture_output=True)
                    if completed_process.returncode == 0:
                        # We received a password from Apple Keychain.
                        password = completed_process.stdout.decode().strip()
                        save_to_keychain = False
                    elif completed_process.returncode == 44:
                        # Apple Keychain told us that no such password was found. Generate one, and stash it in Apple Keychain.
                        password = self.generate_random_password()
                    elif completed_process.returncode == 128:
                        # User cancelled.
                        pass
                    else:
                        click.echo(f'Apple Keychain exit code {completed_process.returncode}:', err=True)
                        click.echo(completed_process.stdout.decode(), err=True)
                        click.echo(completed_process.stderr.decode(), err=True)
                        exit(completed_process.returncode)
                except Exception as ex:
                    click.echo(ex, err=True)
                    pass

        if not password:
            if sys.stdin.isatty():
                password = click.prompt(f'Please enter the encryption password for {self.path}', hide_input=True, err=True)
            else:
                raise RuntimeError(f'We need an encryption password for {self.path}, but stdin is not a TTY (so we cannot expect input).')
        if save_to_keychain:
            completed_process = subprocess.run(['security', 'add-internet-password', '-U', '-a', account, '-s', 'hardcoded', '-l', f'hardcoded {account}', '-T', '', '-w', password,], capture_output=True)
        return password


    def fernet(self, password_policy=None):
        if not self._fernet:
            kdf = PBKDF2HMAC(
                    algorithm=hashes.SHA256(),
                    length=32,
                    salt=self.salt,
                    iterations=1000000,
                    )
            while True:
                password = self.get_password()
                if password_policy:
                    if not password_policy.search(password):
                        click.echo(f'That password does not conform to the password policy regex: {password_policy.pattern}', err=True)
                        self._wrong_password = True
                        continue
                break
            key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
            self._fernet = Fernet(key)
        return self._fernet


    @cached_property
    def _gpg_recipient(self):
        if self._saved_gpg_recipient:
            return self._saved_gpg_recipient
        user_level_datafile = _DataFile(path=DEFAULT_FILE_PATH)
        config_key = 'Default GnuPG encryption key'
        if _saved_gpg_recipient := user_level_datafile.get(config_key):
            self._saved_gpg_recipient = _saved_gpg_recipient
            return self._saved_gpg_recipient

        if not (private_keys := _gpg.list_keys(True)):
            return None

        click.echo('Available GnuPG secret keys:', err=False)
        private_key = None
        for private_key in _gpg.list_keys(True):
            click.echo('\t' + private_key.get('keyid') + '\t' + ' / '.join(private_key.get('uids')), err=False)
        self._saved_gpg_recipient = click.prompt(text='Please choose a default GnuPG key to encrypt hardcoded data with', default=next(iter(private_key.get('uids', [private_key.get('keyid'),]))), err=True)
        user_level_datafile.set(config_key, self._saved_gpg_recipient)
        return self._saved_gpg_recipient



    def encrypt(self, data_bytes):
        if (_gpg != None) and self._gpg_recipient:
            # Prefer encrypting directly with GPG.
            encrypted = _gpg.encrypt(data_bytes, self._gpg_recipient, always_trust=True)
            if encrypted.ok:
                return encrypted.data.decode()
            else:
                raise RuntimeError(
                        f'GPG encryption for {self.path} failed: {encrypted.status}; {encrypted.stderr}')
        elif cryptography_support:
            # Fall back to encrypting with the cryptography library.
            password_policy = re.compile(r'.{8}')
            return self.fernet(password_policy=password_policy).encrypt(data_bytes).decode()
        else:
            if (_gpg != None) and not self._gpg_recipient:
                raise RuntimeError(
                        f'No GPG recipient found and no cryptography library found. Please either generate a GPG keypair or pip install hardcoded[encryption_without_pgp].')
            else:
                raise RuntimeError(
                        f'No GPG found and no cryptography library found. Please either fix your GPG setup or pip install hardcoded[encryption_without_pgp].')


    def decrypt(self, ciphertext):
        if not ciphertext:
            return ''
        if b'BEGIN PGP MESSAGE' in ciphertext:
            if _gpg == None:
                raise RuntimeError(
                        f'{self.path} contains PGP encrypted data. pip install python-gnupg to use it.')
            else:
                decrypted = _gpg.decrypt(ciphertext, always_trust=True)
                if decrypted.ok:
                    return decrypted.data.decode()
                else:
                    raise RuntimeError(
                            f'GPG decryption of {self.path} failed: {decrypted.status}; {decrypted.stderr}')
        elif cryptography_support:
            # Does not look like PGP ciphertext. Assume Fernet.
            return self.fernet().decrypt(ciphertext).decode()
        else:
            raise RuntimeError(
                    f'{self.path} contains symmetrically encrypted data. Please pip install hardcoded[encryption_without_pgp] to be able to decrypt it.')


class File():
    def __init__(self, path=None, secret=True, ask_if_not_found=True, namespace=None):
        '''A file with that data that you're not hardcoding.

        path:    The path to the file. If your code is in a git repository, path is <repo_root>/.hardcoded.yml by default. Otherwise, ~/.hardcoded.yml.
        secret:  If True (the default), encrypt data and try not to put the file on Github.
        ask_if_not_found: If True (the default), the user will be prompted for missing values. Any default value in get() will be presented for easy cofirmation with [enter]. If False, the user will not be prompted for missing values, and any default in get() will be used straight away.
        namespace:        Two programs using the same namespace and the same file path can access each others values. By default, the namespace is based on path.
        '''
        super().__setattr__('__spec__', None)
        super().__setattr__('__name__', 'File')
        super().__setattr__('File', File)
        super().__setattr__('DEFAULT_FILE_NAME', DEFAULT_FILE_NAME)
        super().__setattr__('cli', None)
        super().__setattr__('_x', _OneLayerDeeper())
        self._x.secret = secret
        self._x.ask_if_not_found = ask_if_not_found
        if path and path != NOT_GIVEN:
            path = Path(path).expanduser().resolve()
            self._x.path = path
            self._x._datafile = _DataFile(path=path)
            self._x._namespace = namespace or str(path.parent)
        else:
            # This bit of code is duplicated in __init__.py.
            # This is because of the fact that this code looks at itself and finds the path of the file containing the code.
            caller_path = None
            if path != NOT_GIVEN:
                stack = None
                try:
                    stack = inspect.stack()
                    this_code_file_path = stack[0].filename
                    for frame in stack:
                        caller_path = frame.filename
                        if caller_path != this_code_file_path and 'frozen' not in caller_path.lower():
                            break
                finally:
                    del stack
                repo_root = git.find_repo_path(caller_path)
            else:
                repo_root = None
            if repo_root:
                self._x.path = Path(repo_root) / DEFAULT_FILE_NAME
                self._x._datafile = _DataFile(path=Path(repo_root)/DEFAULT_FILE_NAME)
                self._x._namespace = namespace or 'data'
            else:
                self._x.path = DEFAULT_FILE_PATH
                self._x._datafile = _DataFile(path=DEFAULT_FILE_PATH)
                self._x._namespace = namespace or (caller_path and str(Path(caller_path).parent.resolve())) or 'data'


    def __setattr__(self, name, value):
        code_context = None
        stack = None
        try:
            stack = inspect.stack()
            this_code_file_path = stack[0].filename
            for frame in stack:
                if frame.filename != this_code_file_path and 'frozen' not in frame.filename.lower():
                    code_context = frame.code_context
                    break
        finally:
            del stack
        raise NotImplementedError(
                f'You weren\'t actually trying to hardcode {code_context.pop().strip()}, right? Please implicitly prompt the user for the value of {name} by just trying to use the value of {name}.')


    def __getattr__(self, name):
        return self.get(name)

    def __call__(self, *args, **kwargs):
        return self.get(*args, **kwargs)

    # Using the LRU cache cuts time to do repeated lookups by about 10000%.
    @lru_cache()
    def get(self, name, *, default=None, text=None, type=str):
        '''Get the named variable from the data file.
        If a value with this name doesn't exist and ask_if_not_found is True (the default), prompt the user for the value of a variable to be saved.
        In that case:
        text    may be used to customise the question to the user
        type    ensures that the entered data is saved as a specific data type
        default is the default value offered to the user, and also specifies type.
        '''
        if name in ('__path__', '__file__'):
            return None
        elif name == '__origin__':
            return File

        if environment_variable := os.environ.get(name):
            return type(environment_variable)

        data = self._x.data
        if name in data:
            return data.get(name)

        if (not self._x.ask_if_not_found) and default != None:
            return default

        # Don't try to ask for input if stdin is not a TTY.
        if self._x.ask_if_not_found:
            if sys.stdin.isatty():
                if not text:
                    text = f'Please enter {name} (will be saved in {self._x.path})'
                if type == bool or default in (True, False):
                    # Boolean return value expected. Ask a boolean question.
                    click.echo(text, nl=False, err=True)
                    value = click.getchar(echo=True)
                    while not value in 'yn':
                        click.echo(f'\r{text} [yn]', nl=False, err=True)
                        value = click.getchar(echo=True)
                    click.echo(err=True)
                    value = (value.lower() == 'y')
                else:
                    value = click.prompt(text=text, type=type, default=default, err=True)
                data = self._x.data
                data[name] = value
                self._x.data = data
                return value
            else:
                click.echo(f'We need input ({name}), but stdin is not interactive and environment variable ${name} is empty!', err=True)
                raise KeyError(
                        f'Missing hardcoded.{name}')
        else:
            raise KeyError(
                    f'Missing hardcoded.{name}')


    def dict(self):
        '''Return a dict containing all the keys and values from this file.'''
        return self._x.data

