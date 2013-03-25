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
badd +80 script.py
badd +29 transcribe.py
badd +10 settings.py
badd +2664 gases/helium/boltzmann.txt
badd +50 solvers.py
badd +1 constants.py
badd +41 matrixgen.py
badd +696 gases/helium/electronic.py
badd +548 gases/helium/ralchenko.py
badd +9 gases/helium/states.py
badd +16 initcond.py
badd +12 handler.py
badd +10 sandia.py
badd +1 kushner.py
badd +26 settings/kushner.py
badd +25 gases/helium/rate.py
badd +17 distributions.py
silent! argdel *
edit gases/helium/rate.py
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
exe '1resize ' . ((&lines * 35 + 36) / 72)
exe 'vert 1resize ' . ((&columns * 104 + 103) / 207)
exe '2resize ' . ((&lines * 34 + 36) / 72)
exe 'vert 2resize ' . ((&columns * 104 + 103) / 207)
exe '3resize ' . ((&lines * 35 + 36) / 72)
exe 'vert 3resize ' . ((&columns * 102 + 103) / 207)
exe '4resize ' . ((&lines * 34 + 36) / 72)
exe 'vert 4resize ' . ((&columns * 102 + 103) / 207)
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
let s:l = 22 - ((21 * winheight(0) + 17) / 35)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
22
normal! 036l
wincmd w
argglobal
edit solvers.py
setlocal fdm=manual
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=0
setlocal fml=1
setlocal fdn=20
setlocal fen
silent! normal! zE
let s:l = 1 - ((0 * winheight(0) + 17) / 34)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
1
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
let s:l = 103 - ((34 * winheight(0) + 17) / 35)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
103
normal! 0
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
let s:l = 2575 - ((15 * winheight(0) + 17) / 34)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
2575
normal! 03l
lcd ~/Repos/crammer
wincmd w
2wincmd w
exe '1resize ' . ((&lines * 35 + 36) / 72)
exe 'vert 1resize ' . ((&columns * 104 + 103) / 207)
exe '2resize ' . ((&lines * 34 + 36) / 72)
exe 'vert 2resize ' . ((&columns * 104 + 103) / 207)
exe '3resize ' . ((&lines * 35 + 36) / 72)
exe 'vert 3resize ' . ((&columns * 102 + 103) / 207)
exe '4resize ' . ((&lines * 34 + 36) / 72)
exe 'vert 4resize ' . ((&columns * 102 + 103) / 207)
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
