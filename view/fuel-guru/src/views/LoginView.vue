<template>
  <main id="login-page">
      <div>
        <img src="@/assets/login_avatar.jpg" alt="Avatar Image" id="login-avatar">
      </div>
      <form id="login-form">      
        <div>
          <input placeholder="Username/Email" type="text" v-model="un_e" id="un_e">
        </div>    
        <div>
          <input placeholder="Password" type="password" v-model="pw" id="pw">
        </div>
      </form>
      <!--<div id="res" v-if="signin">
      {{res}}
      </div>-->      
      <div id="login-page-btns">
        <!--sign in to user's page-->
        <div>
          <button id="login-btn" @click="signin">Login</button>
        </div> 
        <div>
          <router-link :to="{name: 'Signup'}" id="login-page-signup">Signup</router-link>
        </div>
        <router-view/>
      </div> 
  </main>
</template>

<script>
export default { 
  data(){
    return {
      un_e:'', 
      pw:''
    }
  },
  methods: {    
    signin() {
      fetch('http://localhost:9000/auth/signin', {        
        body: JSON.stringify({
          "iden": this.un_e, 
          "password": this.pw       
        }),
        method: "POST"
      })
      .then(result => result.json()) //use json intsead of text to get the refresh token
      .then(data => {
        console.log(data); //the data.refresh_token should be in local storage 
      })
      .catch(error => {
        console.log("no")
       // console.log(error);        
      })
    },
  },
  created() {
    this.signin()
  }  
}

/*
export default {
  methods: {
    getGasStations() {
      fetch('http://localhost:9000/auth/signin', {        
        body: JSON.stringify({
          "iden": "johndoe3",
          "password": "John1234$doe"
          //"email": "john3@gmail.com"
          
        }),
        method: "POST"
      })
      .then(result => result.text()) //use json intseal of text to get the refresh token
      .then(data => {
        console.log(data); //the data.refresh_token should be in local storage 
      })
      .catch(error => {
        console.log(error)
      })
    }
  },
created() {
  this.getGasStations()
}
}*/
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
