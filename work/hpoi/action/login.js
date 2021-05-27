console.log(user);
$("body > div.container > form > div:nth-child(2) > div > input").val(user["name"]);
$("body > div.container > form > div:nth-child(3) > div > input").val(user["pwd"]);
$("body > div.container > form > div:nth-child(4) > div > div > label > input[type='checkbox']").click();
$("body > div.container > form > div:nth-child(5) > div > button").click();