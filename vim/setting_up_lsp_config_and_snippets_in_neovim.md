Date: 25-08-2022
# Setting up LSP Config

## What is LSP?

>Language Server Protociol (LSP) is a protocol of communication between
>IDEs/code editors and *servers* that provide programming language specific
>features like code completion, refactoring(renaming variables) or navigating
>to a symbol's definition, etc.

So, there are many code editors like vim, VSCode, Atom, PyCharm, etc. And there
are specific servers that provide features like code completion, navigating to
definition, etc for specific languages. Before LSP was around, most languages
were tied to a given IDE or other editor. Even though the every language needed
stuff like renaming a variable or displaying squigly lines for a possible
error, every IDE had it's own way of implementing that and they had to
implement that for each language.

With LSP, an editor can ask the language server, "Do you support go to
declaration?" and the language server protocol ensures that the way go to
definition APIs follow a standard for all languages. So, any new editor can
make use of any sophisticated language server. And any programmer involved with
the development of a new programming language can make services for that
language available to existing editors. This is the reason Neovim can use the
VSCode's language server (coc) for code diagnostics.

So, editor is the client and servers are any language server providing
information that language. And they communicate with each other using Language
Server Protocol. LSP facilitates features like go-to-definition,
find-references, hover, completion, rename, format, refactor, etc., using
semantic whole-project analysis (unlike |ctags|).

> LSP was developed for VSCode and is now a open standard

Neovim has built-in support as a LSP client but the servers are provided by
third parties. So, you do need to install a language server like pyright in
order to get that auto completion and code diagnostics for python for example.
So, an LSP client does following things:
    * Communicate with server about capabilities (e.g. Can client & server do snippets?)
    * Sends requests and handles responses (e.g. Go-to-definition)
    * Handles notifications sent by server (e.g. Error Diagnostics)

## Now that we know a bit about how LSP works, let's get to setting up LSP configuration for Neovim.
These can be divided into three parts:
* Install nvim-lspconfig
* Install the language server on your PATH
* Tell Neovim to use the language server

### Install nvim-lspconfig
First we need to install nvim-lspconfig plugin which provides configurations
for the Nvim LSP client. So, according to *TJ Devries*, you don't technically
need this plugin, but it helps you manage and connect to the LSP server a bit
more easily. It provides configurations for different language servers to make
it easier to attach and manage them.

To install using VimPlug,
* add the `Plug 'neovim/nvim-lspcnofig'` to your vimrc
  ```vim
  call plug#begin('~/.config/nvim/plugged')
  ...
  Plug 'neovim/nvim-lspconfig' " Configuration for Nvim LSP
  ...
  call plug#end()
  ```
* Restart vim or source your vimrc with `source %`
* And do a `:PlugInstall`

### Install the language server on your PATH
Since I work with python, typescript, I will set up lsp for those.
* Install pyright LSP server for python.
  ```sh
  npm install -g pyright
  ```
* Install typescript-language-server for typescript
  ```sh
  npm install -g typescript typescript-language-server
  ```

### Tell Neovim to use the language server
Now, you have to specify the key maps that you want for the type of functionality
provided by the LSP. and attach them to each of the language server.
* In you vimrc, add the following code
```vim
lua << EOF
-- Mappings.
local opts = { noremap=true, silent=true }

-- Use an on_attach function to only map the following keys
-- after the language server attaches to the current buffer
local on_attach = function(client, bufnr)
    -- Enable completion triggered by <c-x><c-o>
    vim.api.nvim_buf_set_option(bufnr, 'omnifunc', 'v:lua.vim.lsp.omnifunc')

    local bufopts = { noremap=true, silent=true, buffer=bufnr }
    vim.keymap.set('n', 'K', vim.lsp.buf.hover, bufopts)
    vim.keymap.set('n', 'gd', vim.lsp.buf.definition, bufopts)
    vim.keymap.set('n', 'gi', vim.lsp.buf.implementation, bufopts)
    vim.keymap.set('n', 'gr', vim.lsp.buf.references, bufopts)
    vim.keymap.set('n', 'gD', vim.lsp.buf.declaration, bufopts)
    vim.keymap.set('n', '<space>K', vim.lsp.buf.signature_help, bufopts)
    vim.keymap.set('n', 'gt', vim.lsp.buf.type_definition, bufopts)
    vim.keymap.set('n', '<F2>', vim.lsp.buf.rename, bufopts)
    vim.keymap.set('n', '<space>rn', vim.lsp.buf.rename, bufopts)
    vim.keymap.set('n', '<space>ca', vim.lsp.buf.code_action, bufopts)
    vim.keymap.set('n', '<space>f', vim.lsp.buf.formatting, bufopts)
    vim.keymap.set('n', '<space>e', vim.diagnostic.open_float, opts)
    vim.keymap.set('n', '[d', vim.diagnostic.goto_prev, opts)
    vim.keymap.set('n', ']d', vim.diagnostic.goto_next, opts)
end

-- this part is telling neovim to use the lsp server
local servers = { 'pyright', 'tsserver' }
for _, lsp in pairs(servers) do
    require('lspconfig')[lsp].setup {
        on_attach = on_attach,
        flags = {
          debounce_text_changes = 150,
        }
    }
end

-- this is for diagnositcs signs on the line number column
-- use this to beautify the plain E W signs to more fun ones
local signs = { Error = " ", Warn = " ", Hint = " ", Info = " " } 
for type, icon in pairs(signs) do
    local hl = "DiagnosticSign" .. type
    vim.fn.sign_define(hl, { text = icon, texthl= hl, numhl = hl })
end
EOF
```

Now you can go to a python or a javascript project. Yay 🎉🎉🎉

### Notes
* Use `:help lsp` to help with setting up lsp config and learn more about it.
