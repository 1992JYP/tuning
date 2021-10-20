(function(scope) {

    // Getting javascript object prototype's toString function
    var _toString = Object.prototype.toString;
    // Check whether the parameter is Date object or not
    function isDate(o)   { return '[object Date]'   == _toString.call(o); }
    // Check whether the parameter is RegExp object or not
    function isRegExp(o) { return '[object RegExp]' == _toString.call(o); }
    
    function encode(o) {
        return String(o).replace(/[,;"\\=\s%]/g, function (character) {
            return encodeURIComponent(character);
        });
    }
    
    function decode(o) { return decodeURIComponent(o); }

    function isArray(o) { return '[object Array]' == _toString.call(o); }
    
    // Is the given value a plain object / an object whose constructor is `Object`?
    function isPlainObject(o) { return '[object Object]' == _toString.call(o); }

    var Cookie = {
      
      /**
       * Cookie.get(name) -> String | null
       * - name (String): The name of the cookie you want to fetch.
       *
       * Returns the cookie’s value for the passed name, or +null+ if the cookie
       * does not exist.
       */
      get: function get(name) {
        return Cookie.has(name) ? Cookie.list()[name] : null;
      },
      
      /**
       * Cookie.has(name) -> Boolean
       * - name (String): The name of the cookie you want to test the presence of.
       *
       * Returns whether the cookie for that name exists or not.
       */
      has: function has(name) {
        return new RegExp("(?:;\\s*|^)" + encodeURIComponent(name) + '=').test(document.cookie);
      },
      
      /**
       * Cookie.list([nameRegExp]) -> { name: value[, name: value …]}
       * - nameRegExp (RegExp) an optional `RegExp` to filter cookie names.  If anything but
       *   an actual `RegExp` is passed, this argument is ignored.
       *
       * Returns a key-value dictionary of existing cookies for the current page.
       * Note the ordering of names is basically browser-dependent (as in, JS-engine-dependent).
       */
      list: function list(nameRegExp) {
        var pairs = document.cookie.split(';'), pair, result = {};
        for (var index = 0, len = pairs.length; index < len; ++index) {
            pair = pairs[index].split('=');   // key=value pair will be array containing key and value
            pair[0] = pair[0].replace(/^\s+|\s+$/, '');   // remove all the white space in the key name
            if (pair[0].length > 0) {
                if (!isRegExp(nameRegExp) || nameRegExp.test(pair[0]))
                    result[decode(pair[0])] = decode(pair[1]);
            }
        }
        return result;
      },
      
      /**
       * Cookie.remove(name[, options]) -> String
       * - name (String): The name of the cookie you want to remove.
       * - options (Object): An optional set of settings for cookie removal. See Cookie.set for details.
       *
       * Removes the cookie value for the name you passed, honoring potential filtering options.
       * Returns the actual cookie string written to the underlying `document.cookie` property.
       */
      remove: function remove(name, options) {
        var opt2 = {};
        for (var key in (options || {})) opt2[key] = options[key];
        opt2.expires = new Date(0);
        opt2.maxAge = -1;
        return Cookie.set(name, null, opt2);
      },
      
      /**
       * Cookie.empty() -> String
       * - name (String): The name of the cookie you want to remove.
       * - options (Object): An optional set of settings for cookie removal. See Cookie.set for details.
       *
       * Removes all the cookie values
       * Returns if all the cookies are successfully deleted return true otherwise false
       */
      empty: function empty() {
        var keys = Object.keys(Cookie.list());

        for (var i = 0, l = keys.length; i < l; i++) {
            if (Cookie.has(keys[i]))
                Cookie.set(keys[i], '', {'maxAge': -1});
        }

        keys = Object.keys(Cookie.list())

        return keys.length > 0 ? false : true;
      },

      /**
       * Cookie.set(name, value, [, options]) -> String
       * - name (String): The name of the cookie you want to set.
       * - value (Object): The value for the cookie you want to set.  It will undergo a basic `toString()`
       *     transform, so if it's a complex object you likely want to, say, use its JSON representation instead.
       * - options (Object): An optional set of settings for cookie setting. See below.
       *
       * Sets a cookie for the name and value you passed, honoring potential filtering options.
       * Returns the actual cookie string written to the underlying `document.cookie` property.
       *
       * Possible options are:
       *
       * * `path` sets the path within the current domain. Defaults to the current path. Minimum is '/'.
       *   Ignored if blank.
       * * `domain` sets the (sub)domain this cookie pertains to. At the shortest, the current root
       *   domain (e.g. 'example.com'), but can also be any depth of subdomain up to the current one
       *   (e.g. 'www.demo.example.com'). Ignored if blank.
       * * `maxAge` / `max_age` / `max-age` is one way to define when the cookie should expire; this
       *   is a time-to-live in _seconds_. Any of the three keys is accepted, in this order of
       *   decreasing priority (first found key short-circuits the latter ones).
       * * `expires` is the traditional way of setting a cookie expiry, using an absolute GMT date/time
       *   string with an RFC2822 format (e.g. 'Tue, 02 Feb 2010 22:04:47 GMT').  You can also pass
       *   a `Date` object set appropriately, in which case its `toUTCString()` method will be used.
       * * `secure` defines whether the cookie should only be passed through HTTPS connections.  It's
       *   used as `Boolean`-equivalent (so zero, `null`, `undefined` and the empty string are all false).
       * * `samesite` prevents the browser from sending this cookie along with cross-site requests. 
       *   Possible values are lax, strict or none
       */
      set: function set(name, value, options) {
        options = options || {};
        var defList = [encode(name) + '=' + encode(value)];
        if (options.path) defList.push('path=' + options.path);
        if (options.domain) defList.push('domain=' + options.domain);
        var maxAge = 'maxAge' in options ? options.maxAge :
            ('max_age' in options ? options.max_age : options['max-age']), maxAgeNbr;
        if ('undefined' != typeof maxAge && 'null' != typeof maxAge && (!isNaN(maxAgeNbr = parseFloat(maxAge))))
            defList.push('max-age=' + maxAgeNbr);
        var expires = isDate(options.expires) ? options.expires.toUTCString() : options.expires;
        if (expires) defList.push('expires=' + expires);
        if (options.secure) defList.push('secure');
        var sameSiteOptions = ["lax", "strict", "none"];
        if( options.samesite && sameSiteOptions.indexOf(options.samesite) > -1 )
            defList.push('samesite=' + options.samesite);
        else
            defList.push('samesite=' + 'strict');
        defString = defList.join(';');
        document.cookie = defString;
        return defString;
      },
      
      /**
       * Cookie.test() -> Boolean
       * 
       * Tests whether cookies are enabled or not.
       */
      test: function test() {
        var key = '70ab3d39wj3i4j38e2esg74wjefije4eb655b71', value = 'pyg';
        Cookie.remove(key);
        Cookie.set(key, value);
        var result = value == Cookie.get(key);
        Cookie.remove(key);
        return result;
      }
    };
    scope.Cookie = Cookie;
  })(window);