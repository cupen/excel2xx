root_dir:=$(abspath $(CURDIR)/..)
build_dir:=$(root_path)/example/build
excel2xx_bin:=python3 -m excel2xx
excel2xx_bin_debug:=EXCEL2XX_DEBUG=1 python3 -m excel2xx


build: clean
	mkdir -p $(build_dir)
	cd $(root_dir) \
	&& $(excel2xx_bin) json    example/test.xlsx  -o $(build_dir)/test.json \
	&& $(excel2xx_bin) msgpack example/test.xlsx  -o $(build_dir)/test.msgpack \
	&& $(excel2xx_bin) mako    example/test.xlsx  -o $(build_dir)/test.lua --template example/test.lua.mako
	@echo done.


clean:
	rm -fr $(build_dir)
