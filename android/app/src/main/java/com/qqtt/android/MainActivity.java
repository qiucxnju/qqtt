package com.qqtt.android;

import android.app.ProgressDialog;
import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.webkit.CookieManager;
import android.webkit.WebChromeClient;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;

import androidx.appcompat.app.AppCompatActivity;

import java.util.Timer;
import java.util.TimerTask;

public class MainActivity extends AppCompatActivity {
    private WebView webView;
    private ProgressDialog pDialog;
    private String url = "http://www.qqttgroup.com";
    /*
        Handler handler = new Handler(){
            public void handleMessage(Message msg){
                switch(msg.what){
                    case 200:
                        System.out.println("执行我要做的事情用来刷新UI");
                }
            }
        };
    H

        HttpHolder holder = new HttpHolder(handler);
    */
    Timer timer = null;

    @Override
    public void onStart() {
        System.out.println("app start");
        super.onStart();
        timer = new Timer();
        TimerTask cookieTask = new TimerTask() {
            @Override
            public void run() {
                System.out.println("show cookie");
                CookieManager cookieManager = CookieManager.getInstance();
                String cookieStr  = cookieManager.getCookie(url);
                System.out.println(cookieStr);
                SharedPreferences.Editor editor = getSharedPreferences("data",MODE_PRIVATE).edit();
                editor.putString("cookie", cookieStr);
                editor.commit();
            }
        };
        timer.schedule(cookieTask, 0, 10000);

/*
        Intent alarm_intent = new Intent();
        alarm_intent.setAction("ELITOR_CLOCK");
        alarm_intent.setComponent(new ComponentName("com.qqtt.android", "com.qqtt.android.BootBroadcast"));
        PendingIntent pendingIntent = PendingIntent.getBroadcast(getApplicationContext(),
                0, alarm_intent,
                PendingIntent.FLAG_CANCEL_CURRENT);
        AlarmManager am = (AlarmManager)getSystemService(ALARM_SERVICE);
        am.setRepeating(AlarmManager.RTC_WAKEUP,System.currentTimeMillis(),1 * 60 * 1000,pendingIntent);
        System.out.println(getBaseContext());
        stopService(new Intent(getBaseContext(), BackService.class));*/
        startService(new Intent(getBaseContext(), BackService.class));
    }

    @Override
    public void onStop() {
        System.out.println("app stop");
        timer.cancel();
        timer = null;
        super.onStop();
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        //寻找控件的ID
        webView = (WebView) findViewById(R.id.webView);
        //webView加载web资源,打开方式是默认的浏览器
        webView.loadUrl(url);
        webView.addJavascriptInterface(new WebAppInterface(webView.getContext()), "Android");
        //覆盖WebView默认通过第三方或者是系统浏览器打开的行为，使得网页可以在WebView中打开
        webView.setWebViewClient(new WebViewClient() {
            @Override
            public boolean shouldOverrideUrlLoading(WebView view, String url) {
                webView.loadUrl(url);
                //返回值为true的时候控制网页在WebView中打开，为false时调用系统浏览器第三方浏览器
                return false;
            }
        });
        //启用支持JavaScript
        WebSettings settings = webView.getSettings();
        settings.setJavaScriptEnabled(true);
        settings.setTextZoom(50);
        //WebView加载页面优先使用缓存加载
        settings.setCacheMode(WebSettings.LOAD_CACHE_ELSE_NETWORK);
        //页面加载的进度
        webView.setWebChromeClient(new WebChromeClient() {
        });
    }
}
