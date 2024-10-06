local buf = vim.api.nvim_get_current_buf()
local ns = vim.api.nvim_create_namespace("DiwashNS")
print(buf, ns)


-- clearing all extmars and highlights & virtual text
vim.api.nvim_buf_clear_namespace(buf, ns, 0, -1)

local function get_prefix(diag)
    if diag.code == "ERROR" then
        return ""
    end
    if diag.code == "PASS" then
        return ""
    end
    return ""
end

local function add_ghost_text(_buf, text, row, hl)
    vim.api.nvim_buf_set_extmark(_buf, ns, row, -1, {
        virt_text = {{text, hl}},
    })
end

local function add_flag(_buf, line)
    local id = vim.fn.sign_define("Flag", { text = "", texthl = "DiagnosticOk"})
    vim.fn.sign_unplace("")
    vim.fn.sign_place(id, "", "Flag", _buf, {lnum=line})
end


local function mark_test_passed(_buf, text, row)
    add_flag(_buf, row+1)
    add_ghost_text(_buf, "   "..text, row, "DiagnosticOk")
end

local function get_line(pattern, skip_count)
    skip_count = skip_count or 0
    local n_found = 0
    local lines = vim.api.nvim_buf_get_lines(0, 0, -1, false)
    for i, line in ipairs(lines) do
        if string.match(line, pattern) then
            n_found = n_found + 1
            if n_found > skip_count then
                return i
            end
        end
    end
end

function Get3Lines(search_term)
    search_term = search_term or "function"
    local skips = {1, 2, 3}
    local random = math.random(1, 5)
    local offset = math.random(0, 2)
    -- TODO making the following code really obscure by trying to inline everything :D
    return vim.tbl_map(
        function(i)
            return get_line(search_term, i)
        end,
        vim.tbl_map(
            function(n)
                return (n+random) % 3 + offset
            end,
            skips
        )
    )
end

local function get_unique_randoms(count, i_start, i_end)
    local uniques = {}
    for i = 1,count do
        local new_val = nil
        repeat
            new_val = math.random(i_start, i_end)
        until not vim.list_contains(uniques, new_val) or count > i_end - i_start
        uniques[i] = new_val
    end
    return uniques
end

function SetRandomDiagnostics(_buf)
    local _ns = vim.api.nvim_create_namespace("DiwashNS")
    local total_lines = vim.api.nvim_buf_line_count(_buf)
    local nl_1, nl_2, nl_3 = unpack(get_unique_randoms(3, 1, total_lines))
    vim.diagnostic.set(_ns, _buf, {
        {
            bufnr = _buf,
            lnum = nl_1 and nl_1 - 1 or 1,
            end_lnum = nl_1 and nl_1 -1 or 1,
            col = 0,
            end_col = -1,
            severity = vim.diagnostic.severity.WARN,
            message = "Is this working?",
            source = "Diwash",
            code = "ERROR",
        },
        {
            bufnr = _buf,
            lnum = nl_2 and nl_2 - 1 or 2,
            end_lnum = nl_2 and nl_2 - 1 or 2,
            col = 0,
            end_col = -1,
            severity = vim.diagnostic.severity.ERROR,
            message = "False Positive!",
            source = "Diwash",
            code = "ERROR",
        },
    }, {
        virtual_text = {
            spacing = 1,
            prefix = get_prefix,
        },
    })
    vim.api.nvim_buf_clear_namespace(_buf, _ns, 0, -1)
    mark_test_passed(_buf, "Test Passed!", nl_3 - 1)
end

vim.api.nvim_create_autocmd({"BufWritePost"}, {
    group = vim.api.nvim_create_augroup("Walmart Telescopic Johnson", { clear = true }),
    pattern = "*.lua",
    callback = function(event) SetRandomDiagnostics(event.buf) end,
})

