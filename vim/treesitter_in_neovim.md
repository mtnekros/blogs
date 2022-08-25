# Treesitter in neovim

## Why do you need treesitter? 
You may have noticed that for most filetypes, there isn't a really nice syntax
highlighting in vim. Even if you install a specific plugin to deal with a particular
programming languages, you need to keep searching new plugins for the next one
you may need. Similar problems persists for foldings and indentations too. Until
you use treesitter that is.

With treesitter, you will have:
1. Better syntax highlighting for all languages supported by treesitter which is a pretty long list.
2. Better foldings (Because foldings in vim isn't that great to be honest)
3. Better indentations
4. You can even have incremental selections by scope

## Installing Treesitter in Neovim
With VimPlug, installing nvim-treesitter is as easy as adding the following
line to you nvim/init.vim file.

```vim
call plug#begin(~/.config/nvim/plugged')
...
Plug 'nvim-treesitter/nvim-treesitter', {'do': {':TSUpdate'}}
...
call plug#end()
```
Now you can source the rc file with `source %`  or restart the vim. And do a
This will install the nvim-treesitter plugin.

>NOTE: This plugin is only guaranteed to work with specific versions of language
>parsers (as specified in the lockfile.json). When upgrading the plugin, you
>must make sure that all installed parsers are updated to the latest version via
>:TSUpdate

## Language parsers
Now that you have the plugin installed. If you don't install any language
parsers, you won't be able to enjoy the goodness of treesitter magic. You need
to install individual language-parsers for the languages you want to support.
Luckily you can do easily with just a simple command. And it's also supports tabbing
so you can tab through all available language parsers.
```vim
:TSInstall <language_to_install>
```
You can look at the list of all installed packages by using the following command.
```vim
:TSInstallInfo
```

## Modules
There are three main modules in treesitter, each providing a specific
functionality.
1. highlighting
2. folding
3. indentation

These are all disabled by default. In order to enable them, you need to add
the following configurations to you vimrc files

```vim
lua << EOF
require'nvim-treesitter.configs'.setup {
  -- A list of parser names, or "all" 
  ensure_installed = { "c", "lua", "rust", "java", "typescript", "vim", "python", "bash", "markdown" },

  -- Install parsers synchronously (only applied to `ensure_installed`)
  sync_install = false,

  -- Automatically install missing parsers when entering buffer
  -- For eg. if you open a js file in vim, auto_install will automatically install
  -- a parser for that file
  auto_install = true,

  highlight = {
    -- `false` will disable the whole extension
    enable = true,

    -- Setting this to true will run `:h syntax` and tree-sitter at the same time.
    -- Set this to `true` if you depend on 'syntax' being enabled (like for indentation).
    -- Using this option may slow down your editor, and you may see some duplicate highlights.
    -- Instead of true it can also be a list of languages
    additional_vim_regex_highlighting = false,
  },

  -- Incremental selection based on the named nodes from the grammar.
  incremental_selection = {
    enable = true,
    keymaps = {
      init_selection = "gnn",
      node_incremental = "grn",
      scope_incremental = "grc",
      node_decremental = "grm",
    },
  },
  -- Indentation based on treesitter for the = operator NOTE: This is an experimental feature
  indent = {
    enable = true
  }
}
EOF

" use the treesitter grammar for doing automatic folds
set foldmethod=expr
set foldexpr=nvim_treesitter#foldexpr()
```

## Conclusion
So, adding these will ensure that you will now have better highlighting support
for any language inside vim. I specially find the auto_install option to be great
since it install language parser for any file you have opened. I find this to be
incredibly useful whenever I am coding. I hope you find it useful too.
