"use strict";
/*
 * FILE CONTAINS THE FUNCTIONS REQUIRED TO VALIDATE USER INPUT
 */
 let letters = /[a-zA-Z]/g;

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
  str[0].toUpperCase();

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
  let pattern = /^[0-9a-zA-Z_]+$/g;

  if (strLength > 5 && strLength < 30 && str[0].match(letters).length === 1 &&
    str[strLength-1] !== '_' && pattern.test(str) === true) {    
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
 export function valid_email (str) {
  let emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

  if (emailPattern.test(str) == true && letters.test(str[0]) === true) {
    return true
  } else {
    return false
  }
}

/**
 * 
 * @param {String} str 
 * @returns true if the username is password
 * The password must have at least 1 uppercase, 1 lowercase letter, 1 number and 
 * 1 special character. The password must be at least 12 characters.
 */
 export function valid_password (str) {
  let pattern = /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[^a-zA-Z0-9])(?!.*\s).{1,30}$/;
  if (str.match(pattern) && str.length < 30 && str.length > 1) {
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
  