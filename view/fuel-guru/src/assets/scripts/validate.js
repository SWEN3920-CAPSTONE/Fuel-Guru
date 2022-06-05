"use strict";
/**
 * FILE CONTAINS THE FUNCTIONS REQUIRED TO VALIDATE USER INPUT
 */

 let capitalLetters = /[A-Z]/g;
 let commonLetters = /[a-z]/g;
 let numbers = /[0-9]/g;
 let specialChars = /[!-+@^_~]/g;
 let letters = /[a-zA-Z]/g;
 let lettersNumbers = /[0-9a-zA-Z]/g;

/**
 * 
 * @param {String} str 
 * @returns the sanitised string
 */
 export function sanitise_inputs (str) {
  str.replace( /[\(^>+)>/"'&]/g, "");  
  str.replace(/\s+/g, '');
  str.trim();
  return str
}

/**
 * 
 * @param {String} str 
 * @returns true if the string is empty
 */
 export function isEmpty (str) {
  if (str.length == 0 && str === '') {
    return true;
  } else {
    return false;
  }
}

/**
 * 
 * @param {String} str 
 * @returns true if the name is valid
 * The username must contain uppercase letters and lowercase letters only.
 */
 export function valid_name (str) {
  let strLength = str.length;
  let patternLength = str.match(letters).length;

  if (strLength > 2 && strLength < 50 && strLength === patternLength) {
    return true
  } else {
    return false
  }
}

/**
 * 
 * @param {String} str 
 * @returns true if the username is valid
 * The username must contain uppercase letters, lowercase letters, numbers and 
 * underscores only. It must start with a letter and cannot end with an underscore.
 * The length of the username must be greater than 5 and less than 30.
 */
 export function valid_username (str) {
  let strLength = str.length;
  let pattern = /[0-9a-zA-Z_]/g;
  let patternLength = str.match(pattern).length;  

  if (strLength > 5 && strLength < 30 && strLength === patternLength &&
    str[0].match(letters).length === 1 && str[strLength-1] !== '_') {
    return true
  } else {
    return false
  }
}

/**
 * 
 * @param {String} str 
 * @returns true if the email address is valid
 * The email must contain uppercase letters, lowercase letters, numbers, periods,
 * dashes and underscores only. It must start with a letter .
 */
 export function validate_email (str) {
  let strLength = str.length;
  let pattern = /[0-9a-zA-Z_.@-]/g;
  let patternLength = str.match(pattern).length;  
  let emailFormat = /\S+@\S+\.\S+/;

  // checking to see if there is an @ sign in str
  if (str.includes("@")) {
    let lst = str.split("@");
    let username = lst[0];
    let domainInfo = lst[1];

    // checking to see if there is at least one dot (.) in str
    if (str.includes(".")){
      let domainInfoLst = domainInfo.split(".");
      let domainName = domainInfoLst[0];

      if (lst.length === 2 && strLength > 5  && strLength === patternLength &&
        str[0].match(letters).length === 1 && username.length > 5 && username[username-1] !== '_' && 
        username[username-1] !== '-' && username[username-1] !== '.' && domainInfo.length  > 1 && 
        domainInfo.match(specialChars).length === 0 && domainName.match(numbers).length === 0 &&
        domainName[domainName-1] !== '.' && str.test(emailFormat) ) {    
        return true
      } else {
        return false
      }  
    } else {
      return false
    }
  } else {
    return false
  }
}

/**
 * 
 * @param {String} str 
 * @returns true if the username is password
 * The password must have at least 1 uppercase, 1 lowercase letter, 1 number and 1 special character.
 * The password must be at least 12 characters.
 */
 export function valid_password (str) {
  let strLength = str.length;
  //let patternLength = str.match(lettersNumbers).length + str.match(specialChars).length;  

  if (strLength > 11 && strLength < 30 && str.match(capitalLetters).length > 1 && str.match(commonLetters).length > 1 &&
  str.match(numbers).length > 1 && str.match(specialChars).length > 1 &&  str[0].match(specialChars).length === 0) {
    return true
  } else {
    return false
  }
}

/**
 * 
 * @param {String} str 
 * @returns true if the passwords are the same
 * The passwords must be the same to create the user.
 */
 export function confirmPassword (str1, str2) {
  if (str1 === str2 && str1.length === str2.length) {
    return true
  } else {
    return false
  }
}
  