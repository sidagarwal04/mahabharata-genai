<template>
  <v-app style="background-color: #f5f8fc">
    <v-app-bar flat app style="background-color: white">
      <v-avatar :tile="true">
        <img :src="require('@/assets/img/logo.png')" alt="logo" class="mr-3" />
      </v-avatar>
      <v-toolbar-title class="poppins-medium">
        <p class="mb-0 cii-animation-font">Mahabharata Chatbot</p>
        <p class="mb-0 mt-n1" style="font-size: 55%; color: #616161">
          Powered By Neo4j & Google Vertex AI
        </p>
      </v-toolbar-title>
      <v-spacer></v-spacer>

      <v-btn
        fab
        depressed
        x-small
        class="mx-2"
        href="https://www.linkedin.com/in/sidagarwal04/"
        target="_blank"
      >
        <v-icon>mdi-linkedin</v-icon>
      </v-btn>
      <v-btn
        fab
        depressed
        x-small
        class="mx-2"
        href="https://twitter.com/sidagarwal04"
        target="_blank"
      >
        <v-icon>mdi-twitter</v-icon>
      </v-btn>

      <v-chip
        class="poppins-regular d-none d-sm-block d-md-block d-lg-block"
        style="
          background: linear-gradient(90deg, #d56676 0%, #4b84f0 100%);
          color: white;
          cursor: pointer;
        "
      >
        <v-avatar left>
          <v-img :src="require('@/assets/img/user.jpeg')"></v-img>
        </v-avatar>
        Siddhant Agarwal
      </v-chip>
      <v-avatar size="35" class="d-block d-sm-none d-md-none d-lg-none">
        <v-img :src="require('@/assets/img/user.jpeg')"></v-img>
      </v-avatar>
    </v-app-bar>
    <v-main>
      <router-view />
    </v-main>

    <!-- <v-footer
      app
      color="white"
      class="text-center px-md-10 poppins-light"
      style="align-items: center; align-content: center; text-align: center"
    >
      <p class="mb-0" style="font-size: 90%">Powered By Neo4j</p>
      <v-spacer></v-spacer>
      <p class="mb-0" style="font-size: 90%">
        Designed by <a href="https://vrijraj.xyz/" target="_blank">Vrijraj</a>
      </p>
    </v-footer> -->
  </v-app>
</template>

<script>
export default {
  name: "App",

  data: () => ({
    //
  }),
};
</script>
