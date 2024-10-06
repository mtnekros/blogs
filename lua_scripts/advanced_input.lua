-- NOTE: MY GLOBALS
Fidget = require("fidget")

local function get_term_code(key)
	return vim.api.nvim_replace_termcodes(key, true, false, true)
end

local function go_to_normal_mode()
	vim.api.nvim_feedkeys(get_term_code("<ESC>"), "n", true)
end

local function close_window(buf, win)
	if vim.api.nvim_win_is_valid(win) then
		vim.api.nvim_win_close(win, true)
	end
	if vim.api.nvim_buf_is_valid(buf) then
		vim.api.nvim_buf_delete(buf, { force = true })
	end
	go_to_normal_mode()
end

function AddTextToBuf(bufnr, lines)
	vim.api.nvim_buf_set_lines(bufnr, 0, 0, false, lines or { "" })
end

function CreateFloatWindow(title, win_config, texts, buf_options)
	-- Default arguments
	win_config = win_config or {}
	buf_options = vim.tbl_deep_extend("force", { modifiable = true, buftype = "nofile" }, buf_options or {})
	local width = win_config.width or 50
	local height = win_config.height or 10
	local default_opts = {
		title = title,
		title_pos = "center",
		relative = "editor",
		width = 50,
		height = 10,
		col = math.floor((vim.o.columns - width) / 2),
		row = math.floor((vim.o.lines - height) / 2),
		style = "minimal",
		border = "rounded",
	}
	win_config = vim.tbl_deep_extend("force", default_opts, win_config)

	local bufnr = vim.api.nvim_create_buf(false, true)
	local win = vim.api.nvim_open_win(bufnr, true, win_config)

	-- add texts if passed
	if texts ~= nil then
		AddTextToBuf(bufnr, texts)
	end

	-- set options if required
	for opt, value in pairs(buf_options) do
		vim.opt_local[opt] = value
	end

	-- set default quit mechanism
	local quit_map_opts = {
		noremap = true,
		silent = true,
		callback = function()
			close_window(win, bufnr)
		end,
	}
	vim.api.nvim_buf_set_keymap(bufnr, "n", "<ESC>", "", quit_map_opts)
	return { bufnr, win }
end

function CreateSignFlagIfNotExists(sign_name, sign, hl)
	sign_name = sign_name or "SignFlag"
	sign = sign or "⚑"
	hl = hl or "Removed"
	if #vim.fn.sign_getdefined(sign_name) == 0 then
		vim.fn.sign_define("SignFlag", { text = sign, texthl = hl })
	end
	return sign_name
end

function PlaceFlag(bufnr, row)
	local sign_name = CreateSignFlagIfNotExists()
	return vim.fn.sign_place(0, "", sign_name, bufnr, { lnum = row, priority = 10 })
end

function StackedTextInput(prompt, yes_callback, cancel_callback)
	-- for combined container dimensions
	local total_height = 20
	local total_width = 60
	local prompt_height = #prompt + 1
	local margin = 2
	local top = math.floor((vim.o.lines - total_height) / 2)
	local left = math.floor((vim.o.columns - total_width) / 2)
	-- for prompt
	local prompt_win_config = {
		height = prompt_height,
		width = total_width,
		col = left,
		row = top,
	}
	local prompt_buf, prompt_win =
		unpack(CreateFloatWindow(" Prompt ", prompt_win_config, prompt, { modifiable = false }))
	vim.opt_local.modifiable = false
	-- for input box
	local input_win_config = {
		height = total_height - prompt_height,
		width = total_width,
		col = left,
		row = top + prompt_height + margin,
	}
	local input_buf, input_win = unpack(CreateFloatWindow("", input_win_config))
	PlaceFlag(input_buf, 10)

	local function close_input()
		close_window(prompt_buf, prompt_win)
		close_window(input_buf, input_win)
	end

	local function on_submit()
		local lines = vim.api.nvim_buf_get_lines(input_buf, 0, -1, false)
		close_input()
		yes_callback(lines)
	end

	local function on_cancel()
		close_input()
		cancel_callback()
	end

	local augroup = vim.api.nvim_create_augroup("ThisOne", { clear = true })
	vim.api.nvim_create_autocmd({ "BufLeave" }, {
		group = augroup,
		callback = function(event)
			if event.buf == prompt_buf or event.buf == input_buf then
				close_input()
			end
		end,
		once = true,
	})

	-- on success
	vim.api.nvim_buf_set_keymap(input_buf, "n", "<CR>", "", { noremap = true, callback = on_submit })
	-- on cancel
	vim.api.nvim_buf_set_keymap(input_buf, "n", "<ESC>", "", { noremap = true, callback = on_cancel })
end

function Test()
	local prompts = {
		"Enter your notes. ",
		"",
		"To save: Press <ENTER> in normal mode",
		"To cancel: Press <ESC> in normal mode.",
	}
	StackedTextInput(prompts, function(lines)
		Fidget.notify(table.concat(lines, "\n"))
	end, function()
		Fidget.notify("Cancelled!", vim.log.levels.ERROR)
	end)
end

vim.keymap.set("n", "<C-p>", Test)
