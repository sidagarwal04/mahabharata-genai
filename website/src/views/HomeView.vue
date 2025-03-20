<template>
  <v-container fluid class="fill-height">
    <v-row justify="center" align="center">
      <v-col md="6" cols="12" sm="12" order="2" order-sm="2" order-md="1" class="text-center">
        <gradio-app
          style="border: 0 !important; max-height: 400px"
          src="https://sidagarwal04-mahabharata-chatbot.hf.space"
        ></gradio-app>
      </v-col>
      <v-col md="4" cols="12" sm="12" order="1" order-sm="1" order-md="2">
        <v-img :src="require('@/assets/img/logo.png')" width="90"></v-img>
        <p
          class="cii-animation-font poppins-regular text--secondary mb-0"
          style="font-size: 240%; line-height: 44px"
        >
          Unveiling the <br />
          Mahabharata
        </p>
        <p style="font-size: 100%" class="poppins-regular text--secondary mb-4">
          <!-- Delve into the legendary Mahabharata, an epic tale teeming with thousands of characters - heroes and villains, gods and mortals, all intertwined in a web of duty, love, and vengeance. Witness the power of relationships that forge alliances and ignite devastating wars. Explore the complex bonds of brotherhood, the unwavering loyalty of friendship, and the devastating consequences of jealousy and betrayal. Will righteousness prevail, or will darkness consume the land? Dive in and discover the timeless wisdom of the Mahabharata! -->
          The Mahabharata, an ancient Indian epic, explores duty, love, and
          vengeance amidst complex relationships. It asks whether righteousness
          or darkness will prevail, offering timeless wisdom through its
          legendary tale. Dive in and discover the timeless wisdom of the Mahabharata! 

          <!-- A Graph Journey using
          <a
            href="https://neo4j.com/"
            class="cii-animation-font"
            target="_blank"
            >Neo4j</a
          >
          and a building a gen-ai chatbot for exploring the Mahabharata
          Resources -->
        </p>

        <v-btn
          outlined
          x-small
          class="mr-2 mb-2"
          href="https://github.com/sidagarwal04/mahabharata-genai"
          target="_blank"
          rounded
          depressed
          fab
        >
          <v-icon> mdi-github </v-icon>
        </v-btn>
        <v-btn
          depressed
          rounded
          small
          outlined
          class="mr-2 mb-2"
          href="https://sidagarwal04.medium.com/list/mahabharatachatbot-cbf1d049d017"
          target="_blank"
          >Read Blog
          <v-icon right>mdi-open-in-new</v-icon>
        </v-btn>

        <v-btn
          depressed
          rounded
          outlined
          small
          class="mr-2 mb-2"
          href="https://bit.ly/feedback-mbchatbot"
          target="_blank"
          >Feedback
          <v-icon right>mdi-open-in-new</v-icon>
        </v-btn>
        

        <p
          class="my-3 poppins-regular"
          style="font-size: 80%; font-style: italic"
        >
          This tool may display Inaccurate info, double-check its responses.
        </p>
      </v-col>
    </v-row>

    <v-row>
      <v-col
        md="12"
        cols="12"
        sm="12"
        class="text-center poppins-regular"
      
        style="opacity: 0.7"
      >
      <p class="mb-0">Built with ❤️ using <a
            href="https://neo4j.com/"
            class="cii-animation-font"
            target="_blank"
            >Neo4j</a
          >
          and
          <a
            href="https://cloud.google.com/vertex-ai"
            class="cii-animation-font"
            target="_blank"
            >Google Vertex AI</a
          >
        </p>
        <!-- <p class="mb-0" style="font-size: 90%; display: inline">
          Powered By
          <a
            href="https://neo4j.com/"
            class="cii-animation-font"
            target="_blank"
            >Neo4j</a
          >
        </p> -->
        <!-- <span class="mx-2">|</span> -->
        <p class="mb-0" style="font-size: 80%; display: inline">
          Chatbot by
          <a
            href="https://www.linkedin.com/in/sidagarwal04/"
            class="cii-animation-font"
            target="_blank"
            >Siddhant</a
          >
        </p>
        <span class="mx-2">|</span>
        <p class="mb-0" style="font-size: 80%; display: inline">
          Web Design by
          <a
            href="https://vrijraj.xyz/"
            class="cii-animation-font"
            target="_blank"
            >Vrijraj</a
          >
        </p>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  name: "HomePage",
  components: {},
  data: () => ({
    loading: true,
  }),
  created() {
    document.getElementById("component-4").innerHTML = "";
  },
  methods: {
    load() {
      this.loading = false;
    },
  },
};
</script>
