package com.qqtt.android;

import androidx.appcompat.app.AppCompatActivity;

import android.app.ProgressDialog;
import android.webkit.WebChromeClient;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;

import android.os.Bundle;

public class MainActivity extends AppCompatActivity {
    private WebView webView;
    private ProgressDialog pDialog;
    private String url = "http://47.104.100.63";
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        //寻找控件的ID
        webView = (WebView) findViewById(R.id.webView);
        //webView加载web资源,打开方式是默认的浏览器
        webView.loadUrl(url);
        //覆盖WebView默认通过第三方或者是系统浏览器打开的行为，使得网页可以在WebView中打开
        webView.setWebViewClient(new WebViewClient(){
            @Override
            public boolean shouldOverrideUrlLoading(WebView view, String url) {
                webView.loadUrl(url);
                //返回值为true的时候控制网页在WebView中打开，为false时调用系统浏览器第三方浏览器
                return false;
            }
        });
        //启用支持JavaScript
        WebSettings settings=webView.getSettings();
        settings.setJavaScriptEnabled(true);
        settings.setTextZoom(50);
        //WebView加载页面优先使用缓存加载
        settings.setCacheMode(WebSettings.LOAD_CACHE_ELSE_NETWORK);
        //页面加载的进度
        webView.setWebChromeClient(new WebChromeClient(){
        });
    }
}
