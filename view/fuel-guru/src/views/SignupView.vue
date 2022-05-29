<template>
  <main id="signup-page">
    <div>
      <img src="@/assets/login_avatar.jpg" alt="Avatar Image" id="login-avatar">
    </div>      
    <form id="signup-form">
      <div>
        <input type="text" placeholder="Firstname" required ref="fname">
      </div>
      <div>
        <input type="text" placeholder="Lastname" required ref="lname">
      </div>
      <div>
        <input type="email" placeholder="Email Address" required ref="email">
      </div>
      <div>
        <input type="text" placeholder="Username" required ref="uname">
      </div>
      <div>
        <input type="password" placeholder="Password" required ref="pword">
      </div>
      <div>
        <input type="password" placeholder="Comfirm Password" required ref="pword2">
      </div>
      <div>
        <input type="checkbox" id="terms-checkbox" required ref="terms">
        <label for="terms-checkbox">I agree to the terms and conditions.</label>
      </div>
      <div>
        <input type="checkbox" id="age-checkbox" required ref="age">
        <label for="age-checkbox">I am 18 years and older.</label>
      </div>
    </form>
    <div id="signup-page-btns">
        <!--sign in to user's page-->   
        <div>
          <button id="signup-btn">Sign Up</button>
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

<script>
export default {
  methods: {
    getGasStations() {
      fetch('http://localhost:9000/auth/signup', {        
        body: JSON.stringify({
          "username": "johndoe3",
          "password": "John1234$doe",
          "email": "john3@gmail.com",
          "firstname": "Doe",
          "lastname": "John"
        }),
        method: "POST"
      })
      .then(result => result.text())
      .then(data => {
        console.log(data);
      })
      .catch(error => {
        console.log(error)
      })
    }
  },
created() {
  this.getGasStations()
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
