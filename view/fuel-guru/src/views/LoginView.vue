<template>
  <main id="login-page">
      <div>
        <img src="@/assets/login_avatar.jpg" alt="Avatar Image" id="login-avatar">
      </div>
      <form id="login-form">      
        <div>
          <input placeholder="Username" type="text" />
        </div>    
        <div>
          <input placeholder="Password" type="password" />
        </div>
      </form>
      <div id="login-page-btns">
        <!--sign in to user's page-->
        <div>
          <button id="login-btn">Login</button>
        </div> 
        <div>
          <router-link :to="{name: 'Signup'}" id="login-page-signup">Signup / Login</router-link>
        </div>
        <router-view/>
      </div>
  </main>
</template>

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
  padding-top: 5px;
  padding-bottom: 5px;
  padding-left: 4.5%;
  padding-right: 4.5%;
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
</style>
