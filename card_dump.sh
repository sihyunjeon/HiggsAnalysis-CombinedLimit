rm -rf tmp
rm -rf cards
rm -rf workspace
./card_dumper.py --campaign 2016preVFP --channel Electron &
./card_dumper.py --campaign 2016postVFP --channel Electron &
./card_dumper.py --campaign 2017 --channel Electron &
./card_dumper.py --campaign 2018 --channel Electron &
./card_dumper.py --campaign 2016preVFP --channel Muon &
./card_dumper.py --campaign 2016postVFP --channel Muon &
./card_dumper.py --campaign 2017 --channel Muon &
./card_dumper.py --campaign 2018 --channel Muon &
./card_dumper.py --combine

