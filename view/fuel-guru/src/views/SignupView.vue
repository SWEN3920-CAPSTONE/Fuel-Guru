<template>
  <main id="signup-page">
    <div>
      <img src="@/assets/login_avatar.jpg" alt="Avatar Image" id="login-avatar">
    </div>      
    <form id="signup-form">
      <div>
        <input type="text" placeholder="Firstname" required v-model="firstname">
      </div>
      <div>
        <input type="text" placeholder="Lastname" required v-model="lastname">
      </div>
      <div>
        <input type="email" placeholder="Email Address" required v-model="email">
      </div>
      <div>
        <input type="text" placeholder="Username" required v-model="username">
      </div>
      <div>
        <input type="password" placeholder="Password" required v-model="password">
      </div>
      <div>
        <input type="password" placeholder="Comfirm Password" required v-model="password2">
      </div>
      <div>
        <input type="checkbox" id="terms-checkbox" required v-model="confirmTerms">
        <label for="terms-checkbox">I agree to the terms and conditions.</label>
      </div>
      <div>
        <input type="checkbox" id="age-checkbox" required v-model="confirmAge">
        <label for="age-checkbox">I am 18 years and older.</label>
      </div>
    </form>
    <div id="signup-page-btns">
        <!--sign in to user's page-->   
        <div>
          <button id="signup-btn" @click.stop.prevent="signup">Sign Up</button>
        </div> 
        <div>
          Already have an account? 
          <!-- login button-->
          <router-link :to="{name: 'Login'}" id="signup-login"> Login</router-link>
        </div>
    <router-view/>    
    </div>
  </main>
</template>

<script setup>
import {ref} from 'vue';
import router from '../router/index.js';
import {sanitise_inputs, isEmpty, valid_name, valid_username, validate_email, valid_password, confirmPassword} from '../assets/scripts/validate.js'

var firstname = ref('');
var lastname = ref('');
var email = ref('');
var username = ref('');
var password = ref('');
var password2 = ref('');
var confirmTerms = ref(''); //true when checked
var confirmAge = ref(''); //true when checked

const emit = defineEmits(['update']);

function signup() {  
  let message = '';
  // santising the inputs
  firstname.value = sanitise_inputs(firstname.value);
  lastname.value = sanitise_inputs(lastname.value);
  email.value = sanitise_inputs(email.value);
  username.value = sanitise_inputs(username.value);
  password.value = sanitise_inputs(password.value);
  password2.value = sanitise_inputs(password2.value);

  if (isEmpty(firstname.value) === true || isEmpty(lastname.value) === true || isEmpty(email.value) === true || 
  isEmpty(username.value) === true || isEmpty(password.value) === true || isEmpty(password2.value) === true) {
    message = message + "Fill all empty fields. \n";
  } else {
    try {
      if (valid_name(firstname.value) === false && valid_name(lastname.value) === false) {
        message = message + "Invalid name. \n";
      }

      if (valid_username(username.value) === false) {
        message = message + "Invalid username. \n";
      }

      if (validate_email(email.value) === false) {
        message = message + "The username must contain uppercase letters, lowercase letters, numbers and underscores only. It must start with a letter and cannot end with an underscore. \n";
      }

      if (valid_password(password.value) === false && valid_password(password2.value) === false) {
        message = message + "The password must have at least 1 uppercase, 1 lowercase letter, 1 number and 1 special character. The password must be at least 12 characters. \n";
      }

      if (confirmPassword(password.value, password2.value) === false) {
        message = message + "Passwords do not match. \n";
      }

      if (confirmTerms.value === false) {
        message = message + "You must agree to the terms and conditions to complete the signup. \n";
      }

      if (confirmAge.value === false) {
        message = message + "You must confirm your age to complete the signup. \n";
      }
    } catch (error) {
      console.log(error);
    }    
  }  

  if(message ===  '') {
    fetch('http://localhost:9000/auth/signup', {
      body: JSON.stringify({
        "username": username.value,
        "password": password.value,
        "email": email.value,
        "firstname": firstname.value,
        "lastname": lastname.value
      }),
        method: "POST"
      })
      .then(result => result.json()) //use json intsead of text to get the refresh token
      .then(data => {
        console.log(data); //the data.refresh_token should be in local storage 
        if (data.message === "Success") {
          localStorage.setItem('refreshToken', data.refresh_token);
          emit('update');
          router.push({name: 'FuelPrices'});
          alert(`Welcome ${firstname.value}!`);
        }
      })
      .catch(error => {
        console.log(error);        
      })
  } else {
    alert(message);
  }
}
</script>

<style>
#signup-page {
  display: grid;
  grid-template-columns: auto;
  text-align: center;
}

#signup-page-btns div {
  padding-bottom: 10px;
}

#signup-login {
  color:#AA1414;
  text-decoration: underline;
  padding-left: 7px;
}

#signup-form div {
  padding-bottom: 20px;
}

#signup-form {
  padding: 20px;
}

#signup-existing-account {
  display: inline-flex;
  padding-top: 30px;
}

#signup-btn {
  border: 2px solid #AA1414;
  border-radius: 25px;
  padding-top: 5px;
  padding-bottom: 5px;
  padding-left: 7%;
  padding-right: 7%;
  background-color: #AA1414;
  color: white;
}
</style>
