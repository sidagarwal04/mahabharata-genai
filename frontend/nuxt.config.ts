export default defineNuxtConfig({
  devtools: { enabled: true },
  css: ['~/assets/css/main.css'],
  runtimeConfig: {
    public: {
      apiBase: process.env.API_BASE_URL || 'http://localhost:8001'
    }
  },
  app: {
    head: {
      title: 'MAHABHARATA AI SAGE',
      meta: [
        { charset: 'utf-8' },
        { name: 'viewport', content: 'width=device-width, initial-scale=1' },
        { name: 'description', content: 'The Mahabharata, an ancient Indian epic of duty, love, and vengeance. This legendary tale explores complex relationships and the eternal struggle between righteousness and darkness. Dive in and uncover its timeless wisdom.' },
        { name: 'author', content: 'Siddhant Agarwal' },
        { property: 'og:type', content: 'website' },
        { property: 'og:url', content: 'https://mb-aisage.netlify.app/' },
        { property: 'og:title', content: 'Mahabharata AI Sage' },
        { property: 'og:description', content: 'Explore the legends, warriors, and dharma of the Kurukshetra with our AI-powered Mahabharata Sage.' },
        { property: 'og:image', content: 'https://raw.githubusercontent.com/sidagarwal04/mahabharata-genai/refs/heads/main/images/mb_2_0.png' },
        { name: 'twitter:card', content: 'summary_large_image' },
        { name: 'twitter:title', content: 'Mahabharata AI Sage' },
        { name: 'twitter:description', content: 'Explore the legends, warriors, and dharma of the Kurukshetra.' },
        { name: 'twitter:image', content: 'https://raw.githubusercontent.com/sidagarwal04/mahabharata-genai/refs/heads/main/images/mb_2_0.png' }
      ],
      link: [
        { rel: 'icon', type: 'image/x-icon', href: '/favicon.ico?v=2' },
        { rel: 'icon', type: 'image/png', href: '/favicon.png?v=2' }
      ],
      script: [
        {
          src: 'https://www.googletagmanager.com/gtag/js?id=G-W94XSCNS7C',
          async: true
        },
        {
          innerHTML: `
            window.dataLayer = window.dataLayer || [];
            function gtag(){dataLayer.push(arguments);}
            gtag('js', new Date());
            gtag('config', 'G-W94XSCNS7C');
          `,
          type: 'text/javascript'
        },
        {
          innerHTML: JSON.stringify({
            "@context": "https://schema.org",
            "@type": "Organization",
            "url": "https://mb-aisage.netlify.app/",
            "logo": "https://raw.githubusercontent.com/sidagarwal04/mahabharata-genai/refs/heads/main/images/mb_2_0.png",
            "name": "Mahabharata AI Sage"
          }),
          type: 'application/ld+json'
        }
      ]
    }
  }
})
