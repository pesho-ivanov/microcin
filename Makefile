DATA=./lab-data/nastya
GRAPHICS=$(DATA)/graphics

nastya:
	rm -rf $(GRAPHICS)
	mkdir $(GRAPHICS)
	
	./scripts/calc-speeds.py $(DATA)/nastya-apr.json
	#./scripts/calc-speeds.py lab-data/nastya/nastya-apr.json
	
	#montage -geometry '800x600' \
	  $(GRAPHICS)/cells_WT-polyfit-deg2.png \
	  $(GRAPHICS)/cells_import-polyfit-deg1.png \
	  $(GRAPHICS)/cells_inact_import-polyfit-deg1.png \
		$(DATA)/cells_WT-polyfit-deg2.png

	montage -geometry '800x600' \
	  $(GRAPHICS)/OD_WT-polyfit-deg2.png \
	  $(GRAPHICS)/OD_import-polyfit-deg1.png \
	  $(GRAPHICS)/OD_inact_import-polyfit-deg1.png \
		$(DATA)/OD_WT-polyfit-deg2.png

	montage -geometry '800x600' \
	  $(GRAPHICS)/intMcC_WT-gompertz.png \
	  $(GRAPHICS)/intMcC_import-gompertz.png \
	  $(GRAPHICS)/intMcC_inact_import-polyfit-deg2.png \
	  $(GRAPHICS)/extMcC_WT-gompertz.png \
	  $(GRAPHICS)/extMcC_import-polyfit-deg2.png \
	  $(GRAPHICS)/extMcC_inact_import-gompertz.png \
	  	$(DATA)/input-data.png

	montage -geometry '800x600' \
	  $(GRAPHICS)/intMcC_WT.png \
	  $(GRAPHICS)/intMcC_import.png \
	  $(GRAPHICS)/intMcC_inact_import.png \
	  $(GRAPHICS)/extMcC_WT.png \
	  $(GRAPHICS)/extMcC_import.png \
	  $(GRAPHICS)/extMcC_inact_import.png \
          	$(DATA)/normalized-data.png
    
	montage -geometry '800x600' \
	  $(GRAPHICS)/export_rate.png \
	  $(GRAPHICS)/import_rate.png \
	  $(GRAPHICS)/synth_rate.png \
	  $(GRAPHICS)/inactivation_rate.png \
		$(DATA)/speeds.png
