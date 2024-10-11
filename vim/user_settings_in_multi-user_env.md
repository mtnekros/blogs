THIS WORK!!!
```vim
set undofile
set undodir="~/.vim/undo-dir/"

function! ExecuteCmds(cmds)
    for cmd in a:cmds
        execute cmd
    endfor
    echom a:cmds
endfunction

function! NetrwIsOpen()
    for nr in range(1, bufnr('$'))
        if bufname(nr) ==# "NetrwTreeListing" && bufwinid(nr) > 0
            return v:true
        endif
    endfor
    return v:false
endfunction

function! ToggleNetrw()
    let toggleCmds = ["Lexplore"]
    if !NetrwIsOpen()
        let toggleCmds += ["Ntree .", "vertical resize 30"]
    endif
    call ExecuteCmds(toggleCmds)
endfunction

function! MySettings()
    let g:mapleader=" "
    syntax enable
    filetype on
    set rnu nu
    set tabstop=4 softtabstop=4 shiftwidth=4 expandtab shiftround
    set smarttab smartindent
    set hidden
    set list
    set nowrap
    set listchars=eol:⏎,trail:•,tab:‣-
    set nohls
    set incsearch
    set path+=** " Search file recursively with find
    set wildignore+=**/node_modules/**
    set wildignore+=**/venv/**,**/*.pyc,**/*.py~
    set mouse=a " mouse usable on every mode
    set noswapfile
    set undofile
    set splitright
    set wildmenu " enable wildmenus
    set belloff=all⏎ " turn off all annoying bells
    set cursorline⏎
    set colorcolumn=80⏎
    set clipboard=unnamedplus,unnamed⏎
⏎
    " mappings⏎
    nnoremap <leader>l :source ~/.vim/vimrc<CR>:call MySettings()<CR>⏎
⏎
    " window navigation mappings⏎
    " terminal mode⏎
    tnoremap <A-h> <C-\><C-n><C-w>h⏎
    tnoremap <A-j> <C-\><C-n><C-w>j⏎
    tnoremap <A-k> <C-\><C-n><C-w>k⏎
    tnoremap <A-l> <C-\><C-n><C-w>l⏎
    " insert mode⏎
    inoremap <A-h> <C-\><C-n><C-w>h⏎
    inoremap <A-j> <C-\><C-n><C-w>j⏎
    inoremap <A-k> <C-\><C-n><C-w>k⏎
    inoremap <A-l> <C-\><C-n><C-w>l⏎
    " normal mode⏎
    nnoremap <A-h> <C-w>h⏎
    nnoremap <A-j> <C-w>j⏎
    nnoremap <A-k> <C-w>k⏎
    nnoremap <A-l> <C-w>l⏎
⏎
    " netrw mapping⏎
    let g:netrw_liststyle=3⏎
    nnoremap <C-f> :call ToggleNetrw()<CR>⏎
    inoremap <C-f> ^[:call ToggleNetrw()<CR>⏎
⏎
    " highlights⏎
    highlight ExtraWhiteSpace ctermbg=NONE ctermfg=DarkGrey guifg=DarkGrey guibg=NONE⏎
    match ExtraWhiteSpace /\n\|\s\+$\|\t/⏎
    highlight CursorLineNr ctermfg=Grey ctermbg=DarkGrey guibg=DarkGrey guifg=Grey cterm=NONE cterm=bold⏎
    highlight LineNr ctermfg=DarkGrey ctermbg=NONE⏎
    highlight CursorLine ctermbg=DarkGrey cterm=NONE⏎
    hi ColorColumn ctermbg=DarkGrey guibg=DarkGrey⏎
⏎
    echom "Loaded Diwash's Settings"⏎
endfunction⏎
```
