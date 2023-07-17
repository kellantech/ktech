function hash(txt) {
  return CryptoJS.SHA256(txt).toString(CryptoJS.enc.Base64)
}
