local function should_include(_f)
    local ignore_pattern = "^\\.\\|^\\.git\\|^venv\\|__pycache__\\|*\\.py[cod]"
    -- if file name/directory doesn't match, we should include it
    return vim.fn.match(_f, ignore_pattern) == -1
end


function GetAllFilesInDir(dir, _should_include)
    -- local function to check if a file or directory should be ignored
    -- list all directorys except ignored
    local ls_dirs = vim.fn.readdir(dir, _should_include)
    local files = {} -- to store the file directories
    for _, file in pairs(ls_dirs) do
        if vim.fn.isdirectory(dir..'/'..file) == 0  then
            -- if it's a file & not a directory, insert into files table
            table.insert(files, file)
        else
            -- if it's a directory, recursive call this function to get the
            -- files from that directory
            for _, inner_file in pairs(GetAllFilesInDir(dir..'/'..file, _should_include)) do
                table.insert(files, file.."/"..inner_file)
            end
        end
    end
    table.sort(files)
    return files
end


function CreateFloatingWindow(title, texts, buf_opts)
    buf_opts = buf_opts or {}
    local bufnr = vim.api.nvim_create_buf(false, true)
    local width = 60
    local height = 10
    local opts = {
        title = title,
        title_pos = "center",
        relative = "editor",
        width = width,
        height = height,
        col = math.floor((vim.o.columns - width) / 2),
        row = math.floor((vim.o.lines - height) / 2),
        style = "minimal",
        border = "rounded",
    }
    local win = vim.api.nvim_open_win(bufnr, true, opts)
    if texts ~= nil then
        vim.api.nvim_buf_set_lines(bufnr, 0, 10, false, texts)
    end

    for opt, val in pairs(buf_opts) do
        vim.opt_local[opt] = val
    end
    return win, bufnr
end

function CloseWindow(win, buf)
    if (vim.api.nvim_win_is_valid(win)) then
        vim.api.nvim_win_close(win, true)
    end
    if (vim.api.nvim_buf_is_valid(buf)) then
        vim.api.nvim_buf_delete(buf, {force = true})
    end
end

function FindFiles()
    local files = GetAllFilesInDir('.', should_include)
    local win, buf = CreateFloatingWindow(" Find Files ", files, {
        modifiable = false,
        cursorline = true,
    })
    -- vim.opt_local.buftype = "nofile"

    local function open_file()
        local file = vim.fn.getline('.')
        CloseWindow(win, buf)
        vim.cmd("edit " .. file)
    end

    vim.api.nvim_buf_set_keymap(buf, "n", "<esc>", "<cmd>q<cr>", {noremap = true, silent = true})
    vim.api.nvim_buf_set_keymap(buf, "n", "<cr>", "", {noremap = true, silent = true, callback=open_file})
end

vim.keymap.set("n", "<C-p>", FindFiles, {noremap = true, silent = true})
