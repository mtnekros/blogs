Notes = {"THIS IS THE UNEDITED NOTES", "TO CHECK IF IT'S WORKING"}
SignId = nil
IsShowingNote = false
Fidget = require("fidget");

local function get_term_code(key)
    return vim.api.nvim_replace_termcodes(key, true, false, true)
end

local function go_to_normal_mode()
    vim.api.nvim_feedkeys(get_term_code("<ESC>"), "n", true)
end

function CloseWindow(win, buf)
    if (win ~= nil) then
        vim.api.nvim_win_close(win, true)
    end
    if (buf ~= nil) then
        vim.api.nvim_buf_delete(buf, {force = true})
    end
    go_to_normal_mode()
end

function CreateSignFlagIfNotExists()
    local sign_name = "SignFlag"
    if (#vim.fn.sign_getdefined(sign_name) == 0) then
        vim.fn.sign_define("SignFlag", {text = "⚑", texthl="Removed"})
    end
    return sign_name
end


function CreateFloatWindow(title, opts)
    opts = opts or {}
    local width = opts.width or 50;
    local height = opts.height or 10;
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
    opts = vim.tbl_deep_extend("force", default_opts, opts)

    local bufnr = vim.api.nvim_create_buf(false, true)
    local win = vim.api.nvim_open_win(bufnr, true, opts)
    vim.opt_local.modifiable =  true
    vim.opt_local.buftype = "nofile"

    local quit_map_opts = {
        noremap = true,
        silent = true,
        callback = function()
            CloseWindow(win, bufnr)
        end,
    }
    vim.api.nvim_buf_set_keymap(bufnr, "n", "<ESC>", "", quit_map_opts)
    return { bufnr, win }
end

function CreateCursorRelativeWindow(title, opts)
    local default_opts = {
        relative = "cursor",
        col = 1,
        row = 1,
    }
    opts = vim.tbl_deep_extend("force", default_opts, opts or {})
    return CreateFloatWindow(title, opts)
end

function TextInputDialog(title, handle_submit, handle_cancel)
    local width = 50
    local height = 5
    local bufnr, win = unpack(CreateCursorRelativeWindow(title, {width=width, height = height}))
    vim.cmd("startinsert")

    local function on_submit()
        local lines = vim.api.nvim_buf_get_lines(bufnr, 0, -1, false)
        CloseWindow(win, bufnr)
        handle_submit(lines)
    end

    local function on_cancel()
        CloseWindow(win, bufnr)
        handle_cancel()
    end
    -- on success
    vim.api.nvim_buf_set_keymap(bufnr, "n", "<CR>", "", {noremap = true, callback = on_submit})
    vim.api.nvim_buf_set_keymap(bufnr, "n", "<ESC>", "", {noremap = true, callback = on_submit})
    vim.api.nvim_buf_set_keymap(bufnr, "c", "w", "", {noremap = true, callback = on_submit})
    vim.api.nvim_buf_set_keymap(bufnr, "c", "x", "", {noremap = true, callback = on_submit})
    -- on cancel
    vim.api.nvim_buf_set_keymap(bufnr, "c", "q", "", {noremap = true, callback = on_cancel})
end


local function trim_and_join(list, separator)
    local function trim(s) return string.match(s, "^%s*(.-)%s*$") end
    return table.concat(vim.tbl_map(trim, list), separator)
end

function IsNotesEmpty(notes)
    return trim_and_join(notes, "") == ""
end

function AddNote()
    local sign_name = CreateSignFlagIfNotExists()
    local row, col = unpack(vim.api.nvim_win_get_cursor(0))
    local buf = vim.api.nvim_get_current_buf()
    if SignId ~= nil then
        vim.fn.sign_unplace("", {buffer = buf, id = SignId})
    end
    SignId = vim.fn.sign_place(0, '', sign_name, buf, {lnum = row, priority = 10})
    vim.api.nvim_buf_set_mark(0, 'a', row, col, {})

    local function handle_submit(lines)
        Notes = vim.tbl_map(function(l) return string.sub(l, 2, -1) end, lines)
        if IsNotesEmpty(Notes) then
            Fidget.notify("Empty Notes Saved!", vim.log.levels.ERROR)
        else
            Fidget.notify("Notes Saved!")
        end
    end

    local function on_cancel()
        Fidget.notify("Submission Cancelled!", vim.log.levels.ERROR)
    end

    TextInputDialog(" Enter Your Notes ⚑ ", handle_submit, on_cancel)
    vim.opt_local.buftype = "prompt"
    -- Following code will add a prefix in the text input dialog
    local bufnr = vim.api.nvim_get_current_buf()
    vim.fn.sign_place(0, '', sign_name, bufnr, {lnum = 2, priority = 10})
end

function SetIsShowingNote(flag)
    IsShowingNote = flag
end

local function is_marked(key)
    return vim.api.nvim_buf_get_mark(0, key)[1] ~= 0
end

function ShowNote()
    if IsShowingNote then
        return
    end

    SetIsShowingNote(true)
    if (is_marked("a")) then
        vim.cmd("normal! 'a")
    end
    local bufnr, win = unpack(CreateCursorRelativeWindow(" Your Notes: "))
    vim.api.nvim_buf_set_lines(bufnr, 0, -1, false, #Notes > 0 and Notes or {"Nothing to show"})
    vim.opt_local.modifiable = false
    local quit_map_opts = {
        noremap = true,
        callback = function()
            SetIsShowingNote(false)
            CloseWindow(win, bufnr)
        end
    }
    vim.api.nvim_buf_set_keymap(bufnr, "c", "w", "", quit_map_opts)
    vim.api.nvim_buf_set_keymap(bufnr, "c", "q", "", quit_map_opts)
    vim.api.nvim_buf_set_keymap(bufnr, "c", "x", "", quit_map_opts)
    vim.api.nvim_buf_set_keymap(bufnr, "n", "<ESC>", "", quit_map_opts)
end

vim.keymap.set("n", "<C-p>", "<cmd>lua AddNote()<cr>")
vim.keymap.set("n", "<C-n>", "<cmd>lua ShowNote()<cr>")

