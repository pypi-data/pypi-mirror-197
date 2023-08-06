# Configuration on CoCalc

This directory contains files for setting up a project on CoCalc
(cocalc.com).  We do this as follows:

1. We move the default `~/.bashrc` file to `~/.bashrc_cocalc`.
2. We symlink the files in this directory.  This includes a replacement `~/.bashrc`
   which first exports `PATH="~/.local/bin:$PATH` so that upgraded mercurial instances
   can work over SSH, then sources the backup file.
3. We source `~/.bash_aliases_mmf-setup` from `~/.bash_aliases`.

This allows users to customize `~/.bash_aliases` if they need to which is [the default on
   CoCalc](https://doc.cocalc.com/howto/software-development.html?highlight=bash_aliases#is-bashrc-or-bash-profile-called-on-startup)
or customizing the shell.
   
The following features are provided:

* **Terminal command history completion support.** Typing a few
  characters then using the up and down arrows, one should be able to
  scroll through previous terminal commands that have been issued
  starting with these characters.  This is done by providing an
  appropriate [`~/.inputrc`](inputrc) file.  On average, my commands
  are less than 20 characters long, more typically 13 characters.
  Thus, 500000 lines would take somewhere around 6MB.  This allows us
  to have a long history, which we set using `HISTFILESIZE=100000`.
* **Autocompletion.** We have added shell tab-completion for the
  following commands: `pip`, 
* **Mercurial configuration.**  In addition to what is provided by
  running the `mmf_setup` script, a global [`.hgignore`](hgignore) is
  provided with CoCalc-specific ignores and the mercurial username is
  set from the environmental variable `LC_HG_USERNAME`.  For this to
  function, you should set this on your personal computer and forward
  it in your `.ssh/config` file with something like:
  
  ```
  # ~/.ssh/config
    Host cc-project1
      User ff1cb986f...
    
    Host cc*
      HostName ssh.cocalc.com
      ForwardAgent yes
      SetEnv LC_HG_USERNAME=Your Full Name <your.email.address+hg@gmail.com>
      SetEnv LC_GIT_USEREMAIL=your.email.address+git@gmail.com
      SetEnv LC_GIT_USERNAME=Your Full Name
      SetEnv LC_EDITOR=vi
  ```

  The `LC_GIT_USER*` variables perform a similar function for `git` but are set using
  git itself when `mmf_setup` is run.

