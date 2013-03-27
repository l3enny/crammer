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
badd +122 script.py
badd +29 transcribe.py
badd +10 settings.py
badd +124 gases/helium/boltzmann.txt
badd +11 solvers.py
badd +15 constants.py
badd +28 matrixgen.py
badd +2589 gases/helium/electronic.py
badd +548 gases/helium/ralchenko.py
badd +9 gases/helium/states.py
badd +16 initcond.py
badd +12 handler.py
badd +10 sandia.py
badd +1 kushner.py
badd +17 settings/kushner.py
badd +22 gases/helium/rate.py
badd +17 distributions.py
badd +22 settings/sandia.py
badd +14 gases/helium/km.py
badd +15 sc
badd +26 scratch
badd +2 gases/helium/__init__.py
badd +32 visualize.py
badd +1 or
badd +0 dump_order.csv
silent! argdel *
edit visualize.py
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
wincmd _ | wincmd |
split
2wincmd k
wincmd w
wincmd w
set nosplitbelow
set nosplitright
wincmd t
set winheight=1 winwidth=1
exe '1resize ' . ((&lines * 29 + 30) / 61)
exe 'vert 1resize ' . ((&columns * 88 + 89) / 178)
exe '2resize ' . ((&lines * 29 + 30) / 61)
exe 'vert 2resize ' . ((&columns * 88 + 89) / 178)
exe '3resize ' . ((&lines * 19 + 30) / 61)
exe 'vert 3resize ' . ((&columns * 89 + 89) / 178)
exe '4resize ' . ((&lines * 19 + 30) / 61)
exe 'vert 4resize ' . ((&columns * 89 + 89) / 178)
exe '5resize ' . ((&lines * 19 + 30) / 61)
exe 'vert 5resize ' . ((&columns * 89 + 89) / 178)
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
let s:l = 34 - ((13 * winheight(0) + 14) / 29)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
34
normal! 024l
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
let s:l = 211 - ((11 * winheight(0) + 14) / 29)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
211
normal! 037l
wincmd w
argglobal
edit dump_order.csv
setlocal fdm=manual
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=0
setlocal fml=0
setlocal fdn=20
setlocal nofen
silent! normal! zE
let s:l = 1 - ((0 * winheight(0) + 9) / 19)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
1
normal! 030l
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
let s:l = 122 - ((17 * winheight(0) + 9) / 19)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
122
normal! 04l
wincmd w
argglobal
edit settings/sandia.py
setlocal fdm=manual
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=0
setlocal fml=1
setlocal fdn=20
setlocal fen
silent! normal! zE
let s:l = 16 - ((5 * winheight(0) + 9) / 19)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
16
normal! 08l
lcd ~/Repos/crammer
wincmd w
exe '1resize ' . ((&lines * 29 + 30) / 61)
exe 'vert 1resize ' . ((&columns * 88 + 89) / 178)
exe '2resize ' . ((&lines * 29 + 30) / 61)
exe 'vert 2resize ' . ((&columns * 88 + 89) / 178)
exe '3resize ' . ((&lines * 19 + 30) / 61)
exe 'vert 3resize ' . ((&columns * 89 + 89) / 178)
exe '4resize ' . ((&lines * 19 + 30) / 61)
exe 'vert 4resize ' . ((&columns * 89 + 89) / 178)
exe '5resize ' . ((&lines * 19 + 30) / 61)
exe 'vert 5resize ' . ((&columns * 89 + 89) / 178)
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
