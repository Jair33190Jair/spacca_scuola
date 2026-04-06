# Friend-safe copy of the current Zsh setup.
# This keeps the same shell style while avoiding host-specific absolute paths.

export ZSH="$HOME/.oh-my-zsh"

ZSH_THEME="robbyrussell"
plugins=(git)

source "$ZSH/oh-my-zsh.sh"

# Optional: add custom tools to PATH if needed on the target machine.
# export PATH="$HOME/dev/projects/tools/plantuml:$PATH"

# Optional: enable nvm if it is installed.
# export NVM_DIR="$HOME/.nvm"
# [ -s "$NVM_DIR/nvm.sh" ] && . "$NVM_DIR/nvm.sh"
# [ -s "$NVM_DIR/bash_completion" ] && . "$NVM_DIR/bash_completion"

# Optional: enable conda if it is installed.
# if [ -x "$HOME/anaconda3/bin/conda" ]; then
#   __conda_setup="$("$HOME/anaconda3/bin/conda" 'shell.zsh' 'hook' 2> /dev/null)"
#   if [ $? -eq 0 ]; then
#     eval "$__conda_setup"
#   elif [ -f "$HOME/anaconda3/etc/profile.d/conda.sh" ]; then
#     . "$HOME/anaconda3/etc/profile.d/conda.sh"
#   else
#     export PATH="$HOME/anaconda3/bin:$PATH"
#   fi
#   unset __conda_setup
# fi

# Optional: keep your aliases if the claude CLI exists.
alias c='claude --model sonnet'
alias dopus='claude --model opus'
