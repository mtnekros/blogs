# Neovim: 10 Things I Learned When Using Lua In Neovim

## Overview
I recently converted my neovim configuration to completely use lua. I had been using the init.vim. Whenever I need to use lua inside my config files, I just used the lua << EOF ... EOF syntax. After spending some time getting myself used to vimscript, I didn't wanted to just drop it. But everybody and their grand mother was telling me that Lua is the way to go. 

So, a few months ago, I moved all my old config to a backup file and started migrating everything to lua. In this blog, I am list a few things that may trip you up if you are unfamiliar with the lua's way's of doing things.


## Setting Options
`set wrap` is now => `vim.opt.wrap = true`. And negative options like set nowrap is now just `vim.opt.wrap = false`. You can't do `vim.opt.nowrap = true`. Same with the other options like nornu, nonu and so on.

## vim & nvim apis
The function within vim & neovim can be used through the vim.api.somefunc or vim.fn.somefunc. All the nvim functions have the prefix of vim.api.nvim_somefunc. And when you are running this through command mode, you can run in two different ways.

:call readdir('.') or :lua vim.fn.readdir('.')


## Make sure to set up lspconfig & nvim-cmp with cmp-nvim-lua. 
These autocompletes and lsp suggestions has made the transformation much easier. Of course, you can look everything up using the Vim's friendly manual with :help. But LSP & AutoCompletion does make things a lot easier.

## Customization are a lot easier now
Since lua is a "real" programming language that is used extensively in other areas as well. It's easier to find the documentations & help online. It's also an incredibly simple language. You can grasp the main concepts of lua within 20 to 30 minutes and immediately start building utilities for yourself.


# Conclusion
<add conclusion here>

What do you think is the best thing about using lua.
