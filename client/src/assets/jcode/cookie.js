export function setCookie(Cname, value, expire) {
  // eslint-disable-next-line
  var date = new Date();
  date.setSeconds(date.getSeconds() + expire);
  // eslint-disable-next-line
  document.cookie = Cname + '='+escape(value) +'; expires='+date.toGMTString();
  // eslint-disable-next-line
  console.log(document.cookie);
}
// eslint-disable-next-line
export function getCookie(Cname) {
  if (document.cookie.length > 0) {
    // eslint-disable-next-line
    let Cstart = document.cookie.indexOf(Cname + '=');
    if (Cstart !== -1) {
      Cstart = Cstart + Cname.length + 1;
      let Cend = document.cookie.indexOf(';', Cstart);
      if (Cend === -1) Cend = document.cookie.length;
      return unescape(document.cookie.substring(Cstart, Cend));
    }
  }
  return '';
}

export function delCookie(Cname) {
  setCookie(Cname, '', -1);
}
