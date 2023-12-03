#!/bin/bash

perl -pe '$r{one}="1";$r{two}=2;$r{three}=3;$r{four}=4;$r{five}=5;$r{six}=6;$r{seven}=7;$r{eight}=8;$r{nine}=9;my $p=join "|", keys %r; s/(?=($p))/$r{$1}/gm' input.txt | perl -pe 's/[^(0-9)\n]//gm' | perl -pe 's/(?<!^).(?!$)//gm' | perl -pe 's/^.$/$&$&/gm' | paste -s -d'+' | perl -pe 's/\+$//gm' | bc