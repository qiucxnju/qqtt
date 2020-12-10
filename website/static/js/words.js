function search(words){
    url = $(location).attr('href');
    console.log(url);
    url = url.split("?")[0];
    console.log(url);
    $(location).attr('href', url + "?word=" + words);

}
function search_button(element){
    words = $(element).text();
    console.log(words);
    search(words);

}
function search_input(a){
    words = $("#word").val();
    console.log($("#word").val());
    search(words);
    //$(location).attr('href', './?word=' + words);
}
