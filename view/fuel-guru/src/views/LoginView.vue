<template>
  <main id="login-page">
      <div>
        <img src="@/assets/login_avatar.jpg" alt="Avatar Image" id="login-avatar">
      </div>
      <form id="login-form">      
        <div>
          <input placeholder="Username/Email" type="text" v-model="username" id="un_e">
        </div>    
        <div>
          <input placeholder="Password" type="password" v-model="password" id="pw">
        </div>
      </form>
      <!--<div id="res">
      {{response}}
      </div>-->
      <div id="login-page-btns">
        <!--sign in to user's page-->
        <div>
          <button id="login-btn" @click.stop.prevent="login">Login</button>
        </div> 
        <div>
          <router-link :to="{name: 'Signup'}" id="login-page-signup">Signup</router-link>
        </div>
        <router-view/>
      </div> 
  </main>
</template>


<script setup>
import {ref} from 'vue';
import router from '../router/index.js';
import {sanitise_inputs, isEmpty} from '../assets/scripts/validate.js';

const emit = defineEmits(['update']);

var username = ref('');
var password = ref('');

/**
 * Allows a user to log into their account
 */
function login(){
  // santising the inputs
  username.value = sanitise_inputs(username.value);
  password.value = sanitise_inputs(password.value);

if (isEmpty(username.value) === true || isEmpty(password.value) === true) {
    alert("Fill all empty fields.");
} else {
  fetch('http://localhost:9000/auth/signin', {
    body: JSON.stringify({
      "iden": username.value,
      "password": password.value
    }),
      method: "POST",
      headers: {
        Authorization: `Bearer ${localStorage.accessToken}`
      }
    })
    .then(result => result.json()) //use json intsead of text to get the access token
    .then(data => {
      console.log(data); //the data.access_token should be in local storage 
      if (data.message === "Success") {
        localStorage.setItem('accessToken', data.access_token);
        emit('update');
        router.push({name: 'FuelPrices'});
        alert(`Welcome back ${username.value}!`);
      }
      else {         
        alert("Incorrect login credentials!");
      }
    })
    .catch(error => {
      console.log(error);        
    })
  }  
}

/*
          "iden": "johndoe3",
          "password": "John1234$doe"
          //"email": "john3@gmail.com"
        */  
  
</script>


<style>
#login-page {
  display: grid;
  grid-template-columns: auto ;
  text-align: center;
}

#login-form {
  padding-top: 30px;
}

#login-form div {
  padding-bottom: 20px;
}

#login-page-btns { 
  padding-top: 10px;
}

#login-page-btns div { 
  padding-top: 25px;
}

#login-page-signup {
  border: 2px solid #AA1414;
  border-radius: 25px;
  padding-top: 2px;
  padding-bottom: 5px;
  padding-left: 6.5%;
  padding-right: 6.5%;
  color: #AA1414;
  background-color: white;
}

#login-btn {
  border: 2px solid #AA1414;
  border-radius: 25px;
  padding-top: 5px;
  padding-bottom: 5px;
  padding-left: 7%;
  padding-right: 7%;
  background-color: #AA1414;
  color: white;
}

#login-avatar {
  max-height: 150px;
}

#res {
  color: #AA1414;
}
</style>
