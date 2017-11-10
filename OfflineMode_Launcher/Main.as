package
{
'''Main.asをもとに、DropDown2.swfを作成する
'''ライブラリへswfファイルを追加する際は、プロジェクト>プロジェクト設定>Intrinsic Libraries　へ、swfファイルのディレクトリを書く
	App.instance.loaderMgr.loadLibraries(Vector.<String>([
		"guiControlsLobbyBattle.swf"
	]));
	App.utils.classFactory.getComponent("DropdownMenuUI", DropdownMenu);
	import mx.utils.StringUtil;
	import net.wg.gui.components.controls.DropdownMenu;
    import net.wg.infrastructure.base.AbstractWindowView;
    import net.wg.gui.components.controls.SoundButton;
    import flash.text.*;
	import scaleform.clik.data.DataProvider;
	import scaleform.clik.events.*;
	import flash.events.Event;
	import flash.events.MouseEvent;

    public class Main extends AbstractWindowView
    {
        private var soundButtonLoad		: SoundButton;
        private var soundButtonCancel	: SoundButton;
        private var textFieldTest		: TextField;
		private var ddMenu				: DropdownMenu;
		public var mapName : String;
		public var py_log:Function;
		

        public function Main()
        {
            super();
        }

        override protected function onPopulate() : void
        {
            super.onPopulate();
            width = 600;
            height = 400;
            window.title = "Test Window";
			var data : Array = new Array();
			data.push( { label:"00_tank_tutorial" , data:"res/spaces/00_tank_tutorial"} );
			data.push( { label:"01_karelia" , data:"res/spaces/01_karelia" } );
			data.push( { label:"02_malinovka" , data:"res/spaces/02_malinovka"} );
			data.push( { label:"04_himmelsdorf" ,data:"res/spaces/04_himmelsdorf"} );
			data.push( { label:"05_prohorovka" ,data:"res/spaces/05_prohorovka"} );
			data.push( { label:"06_ensk" ,data:"res/spaces/06_ensk"} );
			data.push( { label:"07_lakeville" ,data:"res/spaces/07_lakeville"} );
			data.push( { label:"08_ruinberg" ,data:"res/spaces/08_ruinberg"} );
			data.push( { label:"10_hills" ,data:"res/spaces/10_hills"} );
			data.push( { label:"11_murovanka" ,data:"res/spaces/11_murovanka"} );
			data.push( { label:"13_erlenberg" ,data:"res/spaces/13_erlenberg"} );
			data.push( { label:"14_siegfried_line" ,data:"res/spaces/14_siegfried_line"} );
			data.push( { label:"17_munchen" ,data:"res/spaces/17_munchen"} );
			data.push( { label:"18_cliff" ,data:"res/spaces/18_cliff"} );
			data.push( { label:"19_monastery" ,data:"res/spaces/19_monastery"} );
			data.push( { label:"22_slough" ,data:"res/spaces/22_slough"} );
			data.push( { label:"23_westfield" ,data:"res/spaces/23_westfield"} );
			data.push( { label:"28_desert" ,data:"res/spaces/28_desert"} );
			data.push( { label:"29_el_hallouf" ,data:"res/spaces/29_el_hallouf"} );
			data.push( { label:"31_airfield" ,data:"res/spaces/31_airfield"} );
			data.push( { label:"33_fjord" ,data:"res/spaces/33_fjord"} );
			data.push( { label:"34_redshire" ,data:"res/spaces/34_redshire"} );
			data.push( { label:"35_steppes" ,data:"res/spaces/25_steppes"} );
			data.push( { label:"36_fishing_bay" ,data:"res/spaces/36_fishing_bay"} );
			data.push( { label:"37_caucasus" ,data:"res/spaces/37_caucasus"} );
			data.push( { label:"38_mannerheim_line" ,data:"res/spaces/38_mannerheim_line"} );
			data.push( { label:"44_north_america" ,data:"res/spaces/44_north_america"} );
			data.push( { label:"45_north_america" ,data:"res/spaces/45_north_america"} );
			data.push( { label:"47_canada_a" ,data:"res/spaces/47_canada_a"} );
			data.push( { label:"63_tundra" ,data:"res/spaces/63_tundra"} );
			data.push( { label:"73_asia_korea" ,data:"res/spaces/73_asia_korea"} );
			data.push( { label:"83_kharkiv" , data:"res/spaces/83_kharkiv" } );
			data.push( { label:"84_winter" ,data:"res/spaces/84_winter"} );
			data.push( { label:"86_himmelsdorf" ,data:"res/spaces/86_himmelsdorf"} );
			data.push( { label:"92_starlingrad" ,data:"res/spaces/92_starlingrad"} );
			data.push( { label:"95_lost_city" ,data:"res/spaces/95_lost_city"} );
			data.push( { label:"96_prohorovka_defence" ,data:"res/spaces/96_prohorovka_defence"} );
			data.push( { label:"100_thepit" ,data:"res/spaces/100_thepit"} );
			data.push( { label:"101_dday" ,data:"res/spaces/101_dday"} );
			data.push( { label:"103_ruinberg_winter" ,data:"res/spaces/103_ruinberg_winter"} );
			data.push( { label:"112_eiffel_tower_ctf" ,data:"res/spaces/112_eiffel_tower_ctf"} );
			data.push( { label:"114_czech",data:"res/spaces/114_czech"} );
			data.push( { label:"120_kharkiv_halloween" ,data:"res/spaces/120_kharkiv_halloween"} );
			data.push( { label:"212_epic_random_valley" ,data:"res/spaces/212_epic_random_valley"} );
			data.push( { label:"h03_shopfest_2015" ,data:"res/spaces/h03_shopfest_2015"} );
			data.push( { label:"hangar_bootcamp" ,data:"res/spaces/hangar_bootcamp"} );
			data.push( { label:"hangar_halloween_v2" ,data:"res/spaces/hangar_halloween_v2"} );
			data.push( { label:"hangar_kharkiv_halloween" , data:"res/spaces/hangar_kharkiv_halloween" } );
			data.push( { label:"hangar_premium_v2" ,data:"res/spaces/hangar_premium_v2"} );
			data.push({label:"hangar_v2",data:"res/spaces/hangar_v2"});
			var dataProv : DataProvider = new DataProvider(data);
			textFieldTest = new TextField();
            textFieldTest.width = 580;
            textFieldTest.height = 36;
            textFieldTest.x = 20;
            textFieldTest.y = 15;
            textFieldTest.multiline = true;
            textFieldTest.selectable = false;
            textFieldTest.defaultTextFormat = new TextFormat("$FieldFont", 20, 0xEA4517);
			textFieldTest.text = "If You Select Map Name and Push 'Load' Button, it will load Map.";
			addChild(textFieldTest);
			ddMenu = addChild(App.utils.classFactory.getComponent("DropdownMenuUI", DropdownMenu, {
				x: 20,
				y: 40,
				width: 200,
				itemRenderer: "DropDownListItemRendererSound",
				dropdown: "DropdownMenu_ScrollingList",
				menuRowCount: dataProv.length,
				//rowCount:rows,
				//scrollBar:scrBar,
				dataProvider: dataProv
				//selectedIndex:0
			})) as DropdownMenu;
            soundButtonLoad = addChild(App.utils.classFactory.getComponent("ButtonRed", SoundButton, {
                width: 100,
                height: 25,
                x: 195,
                y: 365,
                label: "Load"
            })) as SoundButton;
			this.soundButtonLoad.addEventListener(MouseEvent.CLICK,this._LoadClick);
            soundButtonCancel = addChild(App.utils.classFactory.getComponent("ButtonNormal", SoundButton, {
                width: 100,
                height: 25,
                x: 305,
                y: 365,
                label: "Cancel"
            })) as SoundButton;
			this.soundButtonCancel.addEventListener(MouseEvent.CLICK,this._CancelClick);
        }
		public function _LoadClick():void
		{
			var _loc3_:* = this.ddMenu.dataProvider[this.ddMenu.selectedIndex];
			this.mapName = _loc3_.data;
			this.onWindowClose();
		}
		public function _CancelClick():void 
		{
			this.onWindowClose();
		}
		public function as_setText():void
		{
			py_log(this.mapName);
		}
      public function as_getName():String{
return this.mapName;
}
    }
}
