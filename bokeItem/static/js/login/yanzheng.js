function changeImg() {
    var arrays =['1','2','3','4','5','6','7','8','9','0',
        'a','b','c','d','e','f','g','h','i','j',
        'k','l','m','n','o','p','q','r','s','t',
        'u','v','w','x','y','z',
        'A','B','C','D','E','F','G','H','I','J',
        'K','L','M','N','O','P','Q','R','S','T',
        'U','V','W','X','Y','Z'];
    code='';
    for(var i=0;i<4;i++){
        var r=parseInt(Math.random()*arrays.length);
        code+=arrays[r];
    }
    document.getElementById('code').innerHTML=code;
}
function check() {
    var input_code=document.getElementById("vcode").value;
    if(input_code.toLowerCase()===code.toLowerCase()){
        return true;
    }else {
        alert("验证码不正确！");
        changeImg();
        return false;
    }
}
