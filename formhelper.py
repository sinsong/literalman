import string
selection = [
(0, 'All Sections'),
(1, '1 - General Commands'),
(2, '2 - System Calls'),
(3, '3 - Subroutines'),
(4, '4 - Special Files'),
(5, '5 - File Formats'),
(6, '6 - Games'),
(7, '7 - Macros and Conventions'),
(8, '8 - Maintenance Commands'),
(9, '9 - Kernel Interface')
#('n', 'n - New Commands')
]

def genselection(selected):
    html = ''
    for s in selection:
        html += string.Template('<option value="$value" $selected>$desc</option>').substitute(value=s[0], desc=s[1], selected=('selected' if s[0] == selected else ''))
    return html