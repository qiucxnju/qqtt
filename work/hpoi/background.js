function readCsv(filename, splitor) {
  var arr = [];
  $.ajax({
    type: "GET",
    url: filename,
    dataType: "text",
    async: false,
    success: function(data) {
      data = data.replace(/\r/g, '');
      csv = data.split('\n');
      title = csv[0].split(splitor);
      //console.log(csv[0]);
      //console.log(title);
      csv.forEach(function(item, index) {
        if (index == 0) return;
        d = item.split(splitor);
        if (d.length != title.length) return;
        jd = {};
        d.forEach(function(item2, index2) {
          //console.log(title[index2]);
          //console.log(title[index2].length);
          jd[title[index2]] = item2;
        });
        //console.log(jd);
        arr.push(jd);
      });
    }
  });
  return arr;
}

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}


async function do_sleep(task) {
  console.log("qcx3");
  sec = parseInt(task['param']);
  console.log("sleep: " + sec);
  return sleep(sec * 1000);
}



function clear_cookies(domain) {
  return promise = new Promise((resolve, reject) => {
    chrome.cookies.getAll({
      domain: domain
    }, function(cookies) {
      promises = [];
      cookies.forEach(function(cookie) {
        console.log("removing " + JSON.stringify(cookie));
        promises.push(new Promise((resolve, reject) => {
          chrome.cookies.remove({
            url: "https://" + domain,
            name: cookie['name']
          }, function() {
            console.log("removd " + JSON.stringify(cookie));
            resolve();
          });
        }));
      });
      Promise.all(promises).then(function() {
        console.log("removdall");
        resolve();
      });
    })
  });
}

function set_cookies(cookie) {
  console.log("setting " + JSON.stringify(cookie));
  return new Promise((resolve, reject) => {
    chrome.cookies.set(cookie, function(cookie) {
      console.log("setted " + JSON.stringify(cookie));
      resolve();
    });
  });
}

function echo_cookie(url, user) {
  console.log("echo " + url);
  return new Promise((resolve, reject) => {
    chrome.cookies.get({
      url: url,
      name: 'utoken'
    }, function(cookie) {
      delete cookie.hostOnly;
      delete cookie.session;
      cookie.url = "https://www.hpoi.net/";
      console.log("[users.csv]\t" + user['index'] + '\t' + user['name'] + '\t' + user['pwd'] + '\tY\t' + JSON.stringify(cookie));
      resolve();
    });
  });
}

async function do_login(task, users) {
  user_id = task['param'];
  user = users[user_id];
  //return echo_cookie('https://www.hpoi.net', user);
  var tab_id;

  return clear_cookies("www.hpoi.net").then(function() {
    return new Promise((resolve, reject) => {
      chrome.tabs.create({
        url: "https://www.hpoi.net/user/login",
        active:false,
      }, function(tab) {
        tab_id = tab.id;
        console.log(tab);
        resolve(tab);
      });
    }).then(function(tab) {
      return new Promise((resolve, reject) => {
        t = tab;
        chrome.tabs.executeScript(tab.id, {
          code: 'var user = ' + JSON.stringify(user)
        }, function() {
          resolve(tab);
        });
      });
    }).then(function(tab) {
      return new Promise((resolve, reject) => {
        chrome.tabs.executeScript(tab.id, {
          file: 'jquery.js'
        }, function(result) {
          resolve(tab);
        });
      });
    }).then(function(tab) {
      return new Promise((resolve, reject) => {
        chrome.tabs.executeScript(tab.id, {
          file: 'action/login.js'
        }, function(result) {
          resolve(tab);
        });
      });
    }).then(function(tab) {
      return do_sleep({
        param: 2
      });
    }).then(function() {
      return echo_cookie('https://www.hpoi.net', user);
    });
  });
}


async function do_give_five(task, users) {

  console.log('giving_five');
  params = task['param'].split(";");
  user_id = params[0];
  id = params[1];
  hobby_id = params[2];
  score = params[3]?parseInt(params[3]):5;
  user = users[user_id];
  url = "https://www.hpoi.net/hobby/" + id;
  console.log(user);
  cookie = JSON.parse(user['cookie']);
  cookie.url = "https://www.hpoi.net/";
  console.log(cookie);

  var tab_id;

  return clear_cookies("www.hpoi.net").then(function() {
    return set_cookies(cookie);
  }).then(function(cookie) {
    return new Promise((resolve, reject) => {
      chrome.tabs.create({
        url: url,
        active:false,
      }, function(tab) {
        tab_id = tab.id;
        console.log(tab);
        resolve(tab);
      });
    });
  }).then(function(tab) {
    return do_sleep({
      param: 5
    });

  }).then(function() {
    return new Promise((resolve, reject) => {
      chrome.tabs.executeScript(tab_id, {
        file: 'jquery.js'
      }, function(result) {
        resolve();
      });
    });
  }).then(function() {
    return new Promise((resolve, reject) => {
      chrome.tabs.executeScript(tab_id, {
        code: 'var data = ' + JSON.stringify({'hobby_id' : hobby_id, score:score, 'task' : task})
      }, function() {
        resolve();
      });
    });
  }).then(function() {
    return new Promise((resolve, reject) => {
      chrome.tabs.executeScript(tab_id, {
        file: 'action/give_five.js'
      }, function(result) {
        console.log("give five");
        console.log(result);
          console.log("[tasks.csv]\t" + task['index'] + '\t' + task['type'] + '\t' + task['param'] + '\t' + result);
        resolve();
      });
    });
  }).then(function() {
    return new Promise((resolve, reject) => {
      chrome.tabs.reload(tab_id, function(result) {
        console.log("reload");
        resolve();
      });
    });
  }).then(function(tab) {
    return do_sleep({
      param: 5
    });

  });

}

async function do_comment_like(task, users) {

  console.log('giving_five');
  params = task['param'].split(";");
  user_id = params[0];
  id = params[1];
  hobby_id = params[2];
  comment_no = params[3];
  comment_id = params[4];
  user = users[user_id];
  url = "https://www.hpoi.net/hobby/" + id;
  console.log(user);
  cookie = JSON.parse(user['cookie']);
  cookie.url = "https://www.hpoi.net/";
  console.log(cookie);

  var tab_id;

  return clear_cookies("www.hpoi.net").then(function() {
    return set_cookies(cookie);
  }).then(function(cookie) {
    return new Promise((resolve, reject) => {
      chrome.tabs.create({
        url: url,
        active:false,
      }, function(tab) {
        tab_id = tab.id;
        console.log(tab);
        resolve(tab);
      });
    });
  }).then(function(tab) {
    return do_sleep({
      param: 5
    });

  }).then(function() {
    return new Promise((resolve, reject) => {
      chrome.tabs.executeScript(tab_id, {
        file: 'jquery.js'
      }, function(result) {
        resolve();
      });
    });
  }).then(function() {
    return new Promise((resolve, reject) => {
      chrome.tabs.executeScript(tab_id, {
        code: 'var data = ' + JSON.stringify({'hobby_id' : hobby_id, 'comment_id':comment_id, 'task' : task})
      }, function() {
        resolve();
      });
    });
  }).then(function() {
    return new Promise((resolve, reject) => {
      chrome.tabs.executeScript(tab_id, {
        file: 'action/comment_like.js'
      }, function(result) {
        console.log("comment like");
        console.log(result);
          console.log("[tasks.csv]\t" + task['index'] + '\t' + task['type'] + '\t' + task['param'] + '\t' + result);
        resolve();
      });
    });
  }).then(function() {
    return new Promise((resolve, reject) => {
      chrome.tabs.reload(tab_id, function(result) {
        console.log("reload");
        resolve();
      });
    });
  }).then(function(tab) {
    return do_sleep({
      param: 5
    });

  });

}


async function do_show(task, users) {

  console.log('show');
  user_id = task['param'];
  user = users[user_id];
  url = "https://www.hpoi.net/index";
  console.log(user);
  cookie = JSON.parse(user['cookie']);
  cookie.url = "https://www.hpoi.net/";
  console.log(cookie);

  var tab_id;

  return clear_cookies("www.hpoi.net").then(function() {
    return set_cookies(cookie);
  }).then(function(cookie) {
    return new Promise((resolve, reject) => {
      chrome.tabs.create({
        url: url,
        active:false,
      }, function(tab) {
        tab_id = tab.id;
        console.log(tab);
        resolve(tab);
      });
    });
  });
  console.log("[tasks.csv]\t" + task['index'] + '\t' + task['type'] + '\t' + task['param'] + '\t 1');

}

async function do_give_comment(task, users) {

  console.log('giving_comment');
  params = task['param'].split(";");
  user_id = params[0];
  id = params[1];
  comment = params[2];
  user = users[user_id];
  url = "https://www.hpoi.net" + id;
  console.log(user);
  cookie = JSON.parse(user['cookie']);
  cookie.url = "https://www.hpoi.net/";
  console.log(cookie);

  var tab_id;

  return clear_cookies("www.hpoi.net").then(function() {
    return set_cookies(cookie);
  }).then(function(cookie) {
    return new Promise((resolve, reject) => {
      chrome.tabs.create({
        url: url,
        active:false,
      }, function(tab) {
        tab_id = tab.id;
        console.log(tab);
        resolve(tab);
      });
    });
  }).then(function(tab) {
    return do_sleep({
      param: 5
    });

  }).then(function() {
    return new Promise((resolve, reject) => {
      chrome.tabs.executeScript(tab_id, {
        file: 'jquery.js'
      }, function(result) {
        resolve();
      });
    });
  }).then(function() {
    return new Promise((resolve, reject) => {
      chrome.tabs.executeScript(tab_id, {
        code: 'var data = ' + JSON.stringify({'comment' : comment, 'task' : task})
      }, function() {
        resolve();
      });
    });
  }).then(function() {
    return new Promise((resolve, reject) => {
      chrome.tabs.executeScript(tab_id, {
        file: 'action/give_comment.js'
      }, function(result) {
        console.log("give comment");
        console.log(result);
          console.log("[tasks.csv]\t" + task['index'] + '\t' + task['type'] + '\t' + task['param'] + '\t' + result);
        resolve();
      });
    });
  });
  /*.then(function() {
    return new Promise((resolve, reject) => {
      chrome.tabs.reload(tab_id, function(result) {
        console.log("reload");
        resolve();
      });
    });
  }).then(function(tab) {
    return do_sleep({
      param: 5
    });

  });
  */

}

async function do_tasks(filename) {

  if (filename){
    filename = "./done/" + filename + ".csv";
  }else{
    filename = "tasks.csv";
  }
  tasks = readCsv(chrome.extension.getURL(filename), '\t');
  users = readCsv(chrome.extension.getURL("users.csv"), '\t');
  user_m = {}
  for (user of users) {
    name = user['name']
    user_m[name] = user
  }
  users = user_m
  console.log(tasks);
  console.log(users);
  for (task of tasks) {
    if (task['status'] != "0") continue;
    console.log(task);
    if (task['type'] == 'give_five') {
      await do_give_five(task, users);
    }else if (task['type'] == 'give_comment') {
      await do_give_comment(task, users);
    }else if (task['type'] == 'comment_like') {
      await do_comment_like(task, users);
    } else if (task['type'] == 'login') {
      await do_login(task, users);
    } else if (task['type'] == 'show') {
      await do_show(task, users);
    } else if (task['type'] == 'sleep') {
      await do_sleep(task);
    }
  }
  console.log("task done");
}

console.log("hello world");
//do_tasks();
/*
// Saves options to chrome.storage
function save_options() {
  var enable = document.getElementById('enable').checked;
  var reimage = document.getElementById('reimage').checked;
  chrome.storage.sync.set({
    enable: enable, 
    reimage: reimage
  }, function() {
    // Update status to let user know options were saved.
    var status = document.getElementById('status');
    status.textContent = 'Options saved.';
    setTimeout(function() {
      status.textContent = '';
    }, 750);
  });
}

// Restores select box and checkbox state using the preferences
// stored in chrome.storage.
function restore_options() {
  // Use default value color = 'red' and likesColor = true.
  chrome.storage.sync.get({
    enable: false,
    reimage: false
  }, function(items) {
    console.log(items);
    document.getElementById('enable').checked = items.enable;
    document.getElementById('reimage').checked = items.reimage;
  });
}
document.addEventListener('DOMContentLoaded', restore_options);
document.getElementById('save').addEventListener('click',
  save_options);
  */