let SessionLoad = 1
if &cp | set nocp | endif
let s:so_save = &so | let s:siso_save = &siso | set so=0 siso=0
let v:this_session=expand("<sfile>:p")
silent only
cd ~/Repos/crammer
if expand('%') == '' && !&modified && line('$') <= 1 && getline(1) == ''
  let s:wipebuf = bufnr('%')
endif
set shortmess=aoO
badd +0 script.py
badd +29 transcribe.py
badd +4 settings.py
badd +2714 gases/helium/boltzmann.txt
badd +3 solvers.py
badd +1 constants.py
badd +34 matrixgen.py
badd +1280 gases/helium/electronic.py
badd +0 gases/helium/ralchenko.py
silent! argdel *
edit settings.py
set splitbelow splitright
wincmd _ | wincmd |
vsplit
1wincmd h
wincmd _ | wincmd |
split
1wincmd k
wincmd w
wincmd w
wincmd _ | wincmd |
split
1wincmd k
wincmd w
set nosplitbelow
set nosplitright
wincmd t
set winheight=1 winwidth=1
exe '1resize ' . ((&lines * 29 + 30) / 61)
exe 'vert 1resize ' . ((&columns * 88 + 89) / 178)
exe '2resize ' . ((&lines * 29 + 30) / 61)
exe 'vert 2resize ' . ((&columns * 88 + 89) / 178)
exe '3resize ' . ((&lines * 29 + 30) / 61)
exe 'vert 3resize ' . ((&columns * 89 + 89) / 178)
exe '4resize ' . ((&lines * 29 + 30) / 61)
exe 'vert 4resize ' . ((&columns * 89 + 89) / 178)
argglobal
setlocal fdm=manual
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=0
setlocal fml=1
setlocal fdn=20
setlocal fen
silent! normal! zE
let s:l = 11 - ((10 * winheight(0) + 14) / 29)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
11
normal! 04l
wincmd w
argglobal
edit gases/helium/electronic.py
setlocal fdm=manual
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=0
setlocal fml=1
setlocal fdn=20
setlocal fen
silent! normal! zE
let s:l = 2596 - ((5 * winheight(0) + 14) / 29)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
2596
normal! 011l
wincmd w
argglobal
edit gases/helium/ralchenko.py
setlocal fdm=manual
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=0
setlocal fml=1
setlocal fdn=20
setlocal fen
silent! normal! zE
let s:l = 512 - ((28 * winheight(0) + 14) / 29)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
512
normal! 0
wincmd w
argglobal
edit script.py
setlocal fdm=manual
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=0
setlocal fml=1
setlocal fdn=20
setlocal fen
silent! normal! zE
let s:l = 52 - ((20 * winheight(0) + 14) / 29)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
52
normal! 0
wincmd w
4wincmd w
exe '1resize ' . ((&lines * 29 + 30) / 61)
exe 'vert 1resize ' . ((&columns * 88 + 89) / 178)
exe '2resize ' . ((&lines * 29 + 30) / 61)
exe 'vert 2resize ' . ((&columns * 88 + 89) / 178)
exe '3resize ' . ((&lines * 29 + 30) / 61)
exe 'vert 3resize ' . ((&columns * 89 + 89) / 178)
exe '4resize ' . ((&lines * 29 + 30) / 61)
exe 'vert 4resize ' . ((&columns * 89 + 89) / 178)
tabnext 1
if exists('s:wipebuf')
  silent exe 'bwipe ' . s:wipebuf
endif
unlet! s:wipebuf
set winheight=1 winwidth=20 shortmess=filnxtToO
let s:sx = expand("<sfile>:p:r")."x.vim"
if file_readable(s:sx)
  exe "source " . fnameescape(s:sx)
endif
let &so = s:so_save | let &siso = s:siso_save
doautoall SessionLoadPost
unlet SessionLoad
" vim: set ft=vim :
