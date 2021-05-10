package com.qqtt.android;

import android.content.Context;
import android.webkit.CookieManager;
import android.webkit.CookieSyncManager;
import android.webkit.JavascriptInterface;

public class WebAppInterface {
    Context mContext;
    WebAppInterface(Context c){
        mContext = c;
    }
    @JavascriptInterface
    public void syncCookie() {

        if (android.os.Build.VERSION.SDK_INT < 21) {
            CookieSyncManager.createInstance(mContext);
        }

        CookieManager cookieManager = CookieManager.getInstance();

        if (android.os.Build.VERSION.SDK_INT >= android.os.Build.VERSION_CODES.LOLLIPOP) {
            cookieManager.flush();
        } else {
            CookieSyncManager.createInstance(mContext);
            CookieSyncManager.getInstance().sync();

        }
    }
}
