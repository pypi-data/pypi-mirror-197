import random, os, sys
import yaclipy as CLI
from .config import Config
from print_ext import PrettyException, Text
from pathlib import Path
from .singleton import Singleton
from .orphan_branch import FileList, OrphanBranch



class FilesNotFound(PrettyException):
    def pretty(self, **kwargs):
        p = Printer()
        p("Files Not found:")
        for f in sorted(self.paths):
            p('  ', f)
        return p



class Vault():

    path = Config.var("The directory that vault commands will manipulate.  The path is relative to the project root.", 'vault/')
    branch = Config.var("The orphan branch name where this vault will live.", 'vault')
    remote = Config.var("The remote where the branch will be pushed.  This lets you keep vaults on a different server from the main branch", 'origin')

    def __init__(self, **kwargs):
        self.ob = OrphanBranch(self.branch(), checkout_path=self.path(), remote=self.remote(), repo='.', **kwargs)
        self.gpg = GPG(**kwargs)
        self._members = None


    def path(self, *args):
        return self.ob.branch_git.repo / Path(*args)


    def members(self, force=False):
        if not self._members or force:
            self._members = [self.gpg.import_key(self.path('members', usr)) for usr in self.path('members').iterdir()]
        return self._members

    
    def files(self, paths=None):
        if not paths: paths = [str(self.repo)]
        paths = [os.path.relpath(p, str(self.repo)) + ('/' if os.path.isdir(p) else '') for p in paths]
        paths = set(p[:-4] if p.endswith('.gpg') else p for p in paths)
        # Initalize tracked, untracked, non-existant
        files = FileSet()
        for f in self.repo.list(invert=True): files.add(f)
        for f in self.repo.list(): files.add(f, File.TRACKED)
        for t,f in self.repo.status(changes_only=True):
            if 'D' in t: files.get(f).flags |= File.REM
        # Collect files matching paths
        used = set()
        fout = []
        for f in sorted(files):
            if p:=f.matches(paths):
                used.add(p)
                fout.append(f)
        if len(used) != len(paths):
            exit(print.ERR, "Files not found:", ['']*3, [f" - {os.path.relpath(f'{self.repo}/{p}')}" for p in set(paths)-used])
        return fout


    def encrypt(self, fname, rm_orig=True):
        if not fname.is_absolute(): fname = self.path(fname)
        users = [c for members in (['-r', u.key] for u in self.members()) for c in members]
        self.gpg('-e', '--yes', '--trust-model', 'always', *users, fname)
        if rm_orig: fname.secure_delete()


    def decrypt(self, fname):
        if not fname.is_absolute(): fname = self.path(fname)
        base = fname.parent
        orig = out = fname.stem
        if (base/out).is_file(): out = out+'.mine'
        try:
            self.gpg('--decrypt', '--yes', '--batch', '--output', base/out, fname)
        except:
            return 'e'
        if orig != out: # Original existed, see if it is actually different
            try:
                Diff()(orig, out, stdout='null')
                File(base/out).secure_delete()
            except:
                return 'c'
        return 'd'
                

    def commit(self):
        dirkeep = set()
        delete = []
        for f in self.files():
            if f&File.REM: delete.append(f)
            fname = os.path.split(str(f))[0]
            dirkeep.add(fname)
            while os.path.basename(fname) != fname:
                dirkeep.add(fname)
                fname = os.path.basename(fname)
        dirkeep.discard('')
        if delete:
            confirm([f'{f:fancy}' for f in delete], ['']*3, '''Are you sure you want to delete these files?
            Deleted files will be lost forever if pushed.
            ~lang ja~これらのファイルを削除してもよろしいですか？
            削除されたファイルは、プッシュされると永久に失われます。''',['']*2,'y/N: ')
        MakeFile(self.path('.gitignore')).replace({'FOLDERS':sorted([f'!/{d}/' for d in dirkeep])}).save()
        self.repo.amend_all('vault')


def ls(*args) -> FileList:
    ''' Show status information about the files in the vault.

    Unlocked files (yellow) are on the disk in a clear-text format.
    For enhanced security they should only be unlocked when needed.::
    
       $ ./cli.py vault lock

    Untracked files (gray) must be added before they can be pushed::

       $ ./cli.py vault lock -a <filename>
    '''
    paths = [self.branch_git.repo] if not paths else [Path(p) for p in paths]
        ####paths = [os.path.relpath(p, str(self.repo)) + ('/' if os.path.isdir(p) else '') for p in paths]
        ####paths = set(p[:-4] if p.endswith('.gpg') else p for p in paths)
    print(args)
    files = Vault().files()
    # Collect files matching paths
    used = set()
    fout = []
    for f in sorted(files):
        if p:=f.matches(paths):
            used.add(p)
            fout.append(f)
    if len(used) != len(paths):
        raise FilesNotFound(paths = set(paths)-used)
    return fout



def members(*, join=False):
    ''' Show the members that can unlock the vault.

    When files are locked, any member listed in the members directory will be able to unlock them.
    To remove a member simple delete their public key from the members directory, then re-lock all of the files. ``vault members --changed``

    Parameters:
        --join
            Add your GPG public key to the vault.
        --changed
            Unlock and re-lock all of the files to accommodate for new or removed members. 
    '''
    member = False
    tbl = Table(0,0)
    for name, email, me, _ in Vault().members():
        member |= me
        tbl((CLR.bld if me else CLR.x, name, CLR.x))
        tbl((' ', CLR.a, f'<{email}>', CLR.x))
    print('',tbl,'')
    if not join: 
        if not member: exit(print.WARN, "You are not a member. Run with ``./cli.py vault members --join`` to join. ~lang ja~あなたはメンバーではない。「--join」で実行すれば参加できる。", )
        return

    def _choose():
        users = list(GPG().list_users())
        if not users: return None
        print.ln("Which user do you want to add to the vault?~lang ja~vaultに参加するユーザーを選択してください：")
        tbl = Table(0,1,0,0, color0=CLR.y, color2=CLR.a, just1='^>', sides=0)
        for i, u in enumerate(users):
            tbl(i+1,')', ' ' + u.name, f' <{u.email}>')
        tbl(i+2, ')', ' Create a new user', '')
        print(tbl)
        while True:
            try:
                uid = int(input(f"? "))
                assert(uid > 0 and uid <= len(users)+1)
                break
            except KeyboardInterrupt:
                print("")
                sys.exit(1)
            except:
                continue
        return None if uid == len(users)+1 else users[uid-1]

    usr = _choose()
    if not usr:
        GPG().genkey()
        usr = _choose()
    mdir = os.path.relpath(Vault().path('members'))
    print.ln(f'''
        Adding public key to `{mdir}`.
        Make sure to `./cli.py vault push` the vault so another member can re-lock the files for you.
        ~lang ja~「{mdir}」に公開鍵を追加します。
         別のメンバーがファイルを再ロックできるように「./cli.py vault push」してください。''')
    GPG().export_key(usr.email, Vault().path('members', usr.email))



def _conflicts(conflict):
    if conflict:
        print.ln(print.ERR, "Conflicts that need to be resolved:~lang ja~解決する必要のある競合：", ['']*3, [f'  - {f}' for f in conflict])


def unlock(*paths, verbose__v=False, quiet=False):
    ''' Unlock one or all the encrypted ``.gpg`` files in the vault.
    ~lang ja~
    vault内の暗号化された「.gpg」ファイルの1つまたはすべてのロックを解除します。

    Parameters:
        [path]
            Files or directories to unlock.  The default is the root vault directory.
            ~lang ja~暗号化を解除するファイルまたはディレクトリ。 デフォルトはルートボールトディレクトリです。
        --verbose, -v
            Show verbose gpg output
        --quiet
            Don't show any output

    Examples:
        Unlock a single file (.gpg is optional)::
           $ ./cli.py vault unlock services/vault/*.txt

        Unlock all files in a directory::
           $ ./cli.py vault unlock services/vault/sub/path/

    '''
    conflict = []
    failed = []
    unlocked = []
    for f in Vault().files(list(paths)):
        if str(f).endswith('.gpg') or not f&File.GPG: continue
        code = Vault().decrypt(f'{f}.gpg', verbose__v)
        {'d':unlocked, 'e':failed, 'c':conflict}[code].append(f)

    if quiet: return
    if unlocked:
        print.ln([f'  {f}' for f in unlocked])
    else:
        print.ln("Nothing unlocked~lang ja~ロックが解除されたものがない")
    if failed:
        print.ln(print.WARN, '''Some files failed to decrypt. These files must be encrypted for you by one of the other members.
        ~lang ja~一部のファイルは復号化に失敗しました。これらのファイルは、他のメンバーが暗号化する必要があります。
        ''', ['']*3, [f'  - {f}' for f in failed])
    _conflicts(conflict)




def lock(*paths, add__a=False, verbose__v=False):
    ''' Lock files and directories.
    ~lang ja~ファイルまたはディレクトリをロックする。

    The .gitignore file by default ignores all files in the vault execpt ``.gpg``
    files.  To add a clear-text file to the vault you must add an appropriate git exception rule to .gitignore.
    ~lang ja~
    .gitignoreファイルは、デフォルトで、.gpgファイル以外すべてのファイルを無視します。
    クリアテキストファイルをvaultに追加するには、適切なgit例外ルールを.gitignoreに追加する必要があります

    Parameters:
        [paths]
            A list of files and directories to lock.  The default is to lock all files in the vault.
            ~lang ja~ロックするファイルまたはディレクトリのリスト。 デフォルトでは、vault内のすべてのファイルがロックされます。
        --verbose, -v
            verbose GPG output
        --add, -a
            Add new files.  By default only files that have been added previouly are locked.
            ~lang ja~新しいファイルを追加します。 デフォルトでは、以前に追加されたファイルのみがロックされます。
    '''
    locked = []
    conflict = []
    for f in Vault().files(paths):
        if f&File.CONFLICT:
            conflict.append(f)
        elif (f&File.GPG and not f&File.NOEXIST) or (add__a and not f&File.TRACKED):
            Vault().encrypt(f)
            locked.append(f)
    if locked:
        print.ln([f'🔒{f}' for f in locked])
    elif not conflict:
        print.ln('Nothing to lock~lang ja~ロックする必要がない')
    _conflicts(conflict)




def push():
    ''' Lock the vault and ``git push`` it to remote origin.
    ~lang ja~
    vaultをロックしてから``git push``する。

    .. warning:

       Don't manually git push the vault contents.
       ~lang ja~
       vaultの内容を手動でgitpushしないでください。

    We don't want to track the file history so we always ``--amend`` and
    force pushing.
    ~lang ja~
    ファイル履歴を追跡したくないので、常に `` --amend``と強制的に押している。
    '''
    lock()
    for f in Vault().files():
        if f&File.CONFLICT:
            exit("Must resolve conflicts before pushing")
    Vault().commit()
    Vault().repo.push(force=True)



def status():
    ''' Show the git status of the repository
    '''
    status = Vault().repo.status()
    print.ln([f'{s} {f}' for s,f in status] if status else 'Up to date')
    print.ln(CLR.o,"Members~lang ja~メンバー",CLR.x, ':')
    members()



def pull():
    ''' Pull from the remote origin.~lang ja~remote originからプルします。

    If you have local changes to clear-text files that you want to merge manually then
    you can manually run git pull::
    ~lang ja~
    手動でマージするクリアテキストファイルにローカルな変更がある場合は、
    手動でgitpullを実行できます::

       $ git -C services/vault pull --rebase
    '''
    unlock(quiet=True)
    Vault().commit()
    Vault().repo.pull_rebase('-X','theirs')
    unlock()
    



def rm(file):
    ''' Write random bytes over the top of a file before deleting it.
    ~lang ja~ファイルを削除する前に、ファイルの上にランダムなバイトを書き込みます。

    This is overkill and probably doesn't help on SSD filesystems.
    ~lang ja~これはやり過ぎであり、SSDファイルシステムではおそらく役に立ちません。

    Parameters:
        <path>, --file <path>
            A file to remove
    '''
    File.rm(file)



@CLI.sub_cmds(ls)
def vault():
    return


