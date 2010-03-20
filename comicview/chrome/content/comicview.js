// (C) 2004 pigworlds
// (C) 2010 Homer Xing
// A helper extension to view media on comic.sjtu.edu.cn

function get_config() {
    var service = Components.classes["@mozilla.org/preferences-service;1"].
                   getService(Components.interfaces.nsIPrefService);   
    var config = service.getBranch("");
    return config
}

function get_mplayer_path() {
    config = get_config();
    try {
        return config.getCharPref('comicview.mplayer_path');
    } catch(error) {
        return '/usr/bin/gmplayer'; // default value
    }
}

function set_mplayer_path(value) {
    config = get_config();
    config.setCharPref('comicview.mplayer_path', value);
}

function init_option_dialog() {
    try {
        var mplayer_path = document.getElementById('mplayer_path');
        mplayer_path.value = get_mplayer_path();
    } catch(err) {
        alert(err);
    }
}

function option_dialog_save() {
    try {
        var mplayer_path = document.getElementById('mplayer_path');
        var value = mplayer_path.value;
        set_mplayer_path(value);
    } catch(err) {
        alert(err);
    }
}

function comicview_init() {
    try {
        context_menu = document.getElementById("contentAreaContextMenu")
        if(context_menu)
            context_menu.addEventListener("popupshowing",hide_menuitems,false);
    } catch(err) {
        alert(err);
    }
}

window.addEventListener("load", comicview_init, false);

function hide_menuitems() {
    try {
        var cm = gContextMenu;
        var hide = ( null == parse_link(cm) );
        document.getElementById("comic-view-mplayer").hidden = hide;
        document.getElementById("comic-view-showurl").hidden = hide;
        document.getElementById("comic-view-separator").hidden = hide;
    } catch(err) {
        alert(err);
    }
}

function parse_link(cm) {
    var url = match_rtsp_mms(cm);
    if (url)
        return url;

    var url = match_vod(cm);
    if (url)
        return url;
    
    return null;
}

//return url for "rtsp:" or "mms:" protocol.
//return null otherwise.
function match_rtsp_mms(cm) {
    if (cm && cm.link) {
        var url = cm.getLinkURL();
        if ( url.match(/^rtsp:|^mms:/i) ) {
        	url = unescape(url);
        	url = utf8_to_unicode(url);
	        // alert(url); //debug
            return url;
        }
    }
    return null;
}

//return url for "vod:" protocol.
//return null otherwise.
function match_vod(cm) {
    if (cm && cm.link && cm.link.getAttribute("onclick")) {
        var jstext = cm.link.getAttribute("onclick");
        // alert(jstext); //debug
        var result = jstext.match(/TruevodPlayEx\('([^']+)','([^']+)','([^']+)'\);/i);
        if (result && result[1] && result[2]) {
            // alert(result[1]); alert(result[2]); //debug
            var url = "vod://"+result[1]+"/"+result[2]; // vod://server:port/medialocation
            url = url.replace(/\\\\/ig, "\\"); // change from javascript sourcecode to real string
            return url;
        }
    }
    return null;
}

function utf8_to_unicode(txt){
    var scriptableUnicodeConverter =
        Components.classes["@mozilla.org/intl/scriptableunicodeconverter"].getService();
    var nsIScriptableUnicodeConverter=scriptableUnicodeConverter.QueryInterface(
        Components.interfaces.nsIScriptableUnicodeConverter);
    nsIScriptableUnicodeConverter.charset = "UTF-8";
    return nsIScriptableUnicodeConverter.ConvertToUnicode(txt);
}

function display_url_in_popup_window() {
    try {
        var cm = gContextMenu;
        var url = parse_link(cm);
        alert(url); // show popup window
    } catch(err) {
        alert(err);
    }
}

function from_unicode(txt, charset){
    var scriptableUnicodeConverter =
        Components.classes["@mozilla.org/intl/scriptableunicodeconverter"].getService();
    var nsIScriptableUnicodeConverter = scriptableUnicodeConverter.QueryInterface(
        Components.interfaces.nsIScriptableUnicodeConverter);
    nsIScriptableUnicodeConverter.charset = charset;
    return nsIScriptableUnicodeConverter.ConvertFromUnicode(txt);
}

function file_exists(path) {
    var file = Components.classes['@mozilla.org/file/local;1']
                .createInstance(Components.interfaces.nsILocalFile);
    file.initWithPath(path);
    return file.exists();
}

function play() {
    try {
        var cm = gContextMenu;
        var url = parse_link(cm);
        //alert(url); //debug
        url = from_unicode(url, 'GB18030');
        //alert(url); //debug
        mplayer_path = get_mplayer_path();
        if( ! file_exists(mplayer_path) ) {
            alert( mplayer_path + 'does not exist.' );
            return
        }

        var mplayer_file = Components.classes['@mozilla.org/file/local;1']
                            .createInstance(Components.interfaces.nsILocalFile);
        mplayer_file.initWithPath(mplayer_path);
        var process = Components.classes['@mozilla.org/process/util;1']
                      .createInstance(Components.interfaces.nsIProcess);
        process.init(mplayer_file);
        var argv = [] ;
        argv.push(url);
        process.run(false, argv, argv.length, {});
    } catch(err) {
        alert(err);
    }
}

