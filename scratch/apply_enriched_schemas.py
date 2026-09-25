import re
import json
import os

BASE_DIR = r"c:\Users\Usuario\Documents\GitHub\MariaPaulaConfiteria"

SCHEMAS = {
    "index.html": """    <!-- ═══════════════════════════════════════════ -->
    <!--  DATOS ESTRUCTURADOS SCHEMA.ORG (JSON-LD)   -->
    <!-- ═══════════════════════════════════════════ -->
    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": ["Bakery", "CafeOrCoffeeShop", "Restaurant"],
      "name": "María Paula Confitería",
      "alternateName": "María Paula",
      "image": "https://mariapaulaconfiteria.com/assets/images/logo-maria-paula-confiteria.png",
      "logo": "https://mariapaulaconfiteria.com/assets/images/logo-maria-paula-confiteria.png",
      "url": "https://mariapaulaconfiteria.com/",
      "telephone": "+541146677707",
      "email": "1301mpaula@gmail.com",
      "priceRange": "$3.000 - $22.000 ARS",
      "currenciesAccepted": "ARS",
      "paymentAccepted": "Efectivo, Tarjeta de Débito, Tarjeta de Crédito, Mercado Pago",
      "hasMenu": "https://mariapaulaconfiteria.com/menu/",
      "acceptsReservations": "True",
      "servesCuisine": [
        "Pastelería Artesanal",
        "Cafetería de Especialidad",
        "Panadería",
        "Cocina Tradicional Argentina",
        "Heladería"
      ],
      "address": {
        "@type": "PostalAddress",
        "streetAddress": "Consejal Tribulato 1148",
        "addressLocality": "San Miguel",
        "addressRegion": "Buenos Aires",
        "postalCode": "B1663",
        "addressCountry": "AR"
      },
      "openingHoursSpecification": [
        {
          "@type": "OpeningHoursSpecification",
          "dayOfWeek": [
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
            "Sunday"
          ],
          "opens": "06:00",
          "closes": "22:00"
        }
      ],
      "department": [
        {
          "@type": ["Bakery", "CafeOrCoffeeShop", "Restaurant"],
          "name": "María Paula Confitería – Sucursal Tribulato",
          "telephone": "+541146677707",
          "url": "https://mariapaulaconfiteria.com/sucursal-tribulato/",
          "address": {
            "@type": "PostalAddress",
            "streetAddress": "Consejal Tribulato 1148",
            "addressLocality": "San Miguel",
            "addressRegion": "Buenos Aires",
            "postalCode": "B1663",
            "addressCountry": "AR"
          },
          "openingHoursSpecification": [
            {
              "@type": "OpeningHoursSpecification",
              "dayOfWeek": [
                "Monday",
                "Tuesday",
                "Wednesday",
                "Thursday",
                "Friday",
                "Saturday",
                "Sunday"
              ],
              "opens": "06:00",
              "closes": "22:00"
            }
          ]
        },
        {
          "@type": ["Bakery", "CafeOrCoffeeShop", "Restaurant"],
          "name": "María Paula Confitería – Sucursal Balbín",
          "telephone": "+541144518282",
          "url": "https://mariapaulaconfiteria.com/sucursal-balbin/",
          "address": {
            "@type": "PostalAddress",
            "streetAddress": "Av. Dr. Ricardo Balbín 1301",
            "addressLocality": "San Miguel",
            "addressRegion": "Buenos Aires",
            "postalCode": "B1663",
            "addressCountry": "AR"
          },
          "openingHoursSpecification": [
            {
              "@type": "OpeningHoursSpecification",
              "dayOfWeek": [
                "Monday",
                "Tuesday",
                "Wednesday",
                "Thursday",
                "Friday",
                "Saturday",
                "Sunday"
              ],
              "opens": "06:00",
              "closes": "22:00"
            }
          ]
        }
      ],
      "sameAs": [
        "https://www.instagram.com/mariapaulaconfiteria/?hl=es",
        "https://www.facebook.com/profile.php?id=100048064763939",
        "https://wa.me/5491135433031"
      ]
    }
    </script>
    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": "VideoObject",
      "name": "Cafetería y Pastelería Artesanal en San Miguel - María Paula",
      "description": "Recorrido audiovisual por las especialidades de cafetería, medialunas y pastelería artesanal tradicional de María Paula Confitería.",
      "thumbnailUrl": "https://mariapaulaconfiteria.com/assets/images/video-hero-poster.webp",
      "uploadDate": "2024-01-15T08:00:00-03:00",
      "contentUrl": "https://mariapaulaconfiteria.com/assets/videos/hero-loop.mp4",
      "embedUrl": "https://mariapaulaconfiteria.com/assets/videos/hero-loop.mp4"
    }
    </script>""",

    "sucursal-tribulato/index.html": """    <!-- ═══════════════════════════════════════════ -->
    <!--  DATOS ESTRUCTURADOS SCHEMA.ORG (JSON-LD)   -->
    <!-- ═══════════════════════════════════════════ -->
    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": ["Bakery", "CafeOrCoffeeShop", "Restaurant"],
      "name": "María Paula Confitería – Sucursal Tribulato",
      "image": "https://mariapaulaconfiteria.com/assets/images/salon-moderno-sucursal-tribulato-san-miguel-desktop.webp",
      "logo": "https://mariapaulaconfiteria.com/assets/images/logo-maria-paula-confiteria.png",
      "url": "https://mariapaulaconfiteria.com/sucursal-tribulato/",
      "telephone": "+541146677707",
      "email": "1301mpaula@gmail.com",
      "hasMenu": "https://mariapaulaconfiteria.com/menu/",
      "priceRange": "$3.000 - $22.000 ARS",
      "currenciesAccepted": "ARS",
      "paymentAccepted": "Efectivo, Tarjeta de Débito, Tarjeta de Crédito, Mercado Pago",
      "servesCuisine": [
        "Pastelería Artesanal",
        "Cafetería de Especialidad",
        "Panadería",
        "Cocina Tradicional Argentina",
        "Helados Artesanales"
      ],
      "acceptsReservations": "True",
      "potentialAction": {
        "@type": "ReserveAction",
        "target": {
          "@type": "EntryPoint",
          "urlTemplate": "https://wa.me/5491135433031?text=Hola,%20escribo%20desde%20la%20web%20MariaPaulaConfiteria.com.%20Quiero%20hacer%20una%20reserva%20para%20la%20sucursal%20de%20Tribulato."
        },
        "result": {
          "@type": "FoodEstablishmentReservation"
        }
      },
      "parentOrganization": {
        "@type": "Organization",
        "name": "María Paula Confitería",
        "url": "https://mariapaulaconfiteria.com/"
      },
      "address": {
        "@type": "PostalAddress",
        "streetAddress": "Consejal Tribulato 1148",
        "addressLocality": "San Miguel",
        "addressRegion": "Buenos Aires",
        "postalCode": "B1663",
        "addressCountry": "AR"
      },
      "geo": {
        "@type": "GeoCoordinates",
        "latitude": -34.5427,
        "longitude": -58.7126
      },
      "openingHoursSpecification": [
        {
          "@type": "OpeningHoursSpecification",
          "dayOfWeek": [
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
            "Sunday"
          ],
          "opens": "06:00",
          "closes": "22:00"
        }
      ],
      "sameAs": [
        "https://www.instagram.com/mariapaulaconfiteria/?hl=es",
        "https://www.facebook.com/profile.php?id=100048064763939",
        "https://wa.me/5491135433031"
      ]
    }
    </script>""",

    "sucursal-balbin/index.html": """    <!-- ═══════════════════════════════════════════ -->
    <!--  DATOS ESTRUCTURADOS SCHEMA.ORG (JSON-LD)   -->
    <!-- ═══════════════════════════════════════════ -->
    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": ["Bakery", "CafeOrCoffeeShop", "Restaurant"],
      "name": "María Paula Confitería – Sucursal Balbín",
      "image": "https://mariapaulaconfiteria.com/assets/images/salon-clasico-sucursal-balbin-san-miguel-desktop.webp",
      "logo": "https://mariapaulaconfiteria.com/assets/images/logo-maria-paula-confiteria.png",
      "url": "https://mariapaulaconfiteria.com/sucursal-balbin/",
      "telephone": "+541144518282",
      "email": "1301mpaula@gmail.com",
      "hasMenu": "https://mariapaulaconfiteria.com/menu/",
      "priceRange": "$3.000 - $22.000 ARS",
      "currenciesAccepted": "ARS",
      "paymentAccepted": "Efectivo, Tarjeta de Débito, Tarjeta de Crédito, Mercado Pago",
      "servesCuisine": [
        "Pastelería Artesanal",
        "Cafetería de Especialidad",
        "Panadería",
        "Cocina Porteña Tradicional"
      ],
      "acceptsReservations": "True",
      "potentialAction": {
        "@type": "ReserveAction",
        "target": {
          "@type": "EntryPoint",
          "urlTemplate": "https://wa.me/5491135433031?text=Hola,%20escribo%20desde%20la%20web%20MariaPaulaConfiteria.com.%20Quiero%20hacer%20una%20reserva%20para%20la%20sucursal%20de%20Balb%C3%ADn."
        },
        "result": {
          "@type": "FoodEstablishmentReservation"
        }
      },
      "parentOrganization": {
        "@type": "Organization",
        "name": "María Paula Confitería",
        "url": "https://mariapaulaconfiteria.com/"
      },
      "address": {
        "@type": "PostalAddress",
        "streetAddress": "Av. Dr. Ricardo Balbín 1301",
        "addressLocality": "San Miguel",
        "addressRegion": "Buenos Aires",
        "postalCode": "B1663",
        "addressCountry": "AR"
      },
      "geo": {
        "@type": "GeoCoordinates",
        "latitude": -34.5372,
        "longitude": -58.7089
      },
      "openingHoursSpecification": [
        {
          "@type": "OpeningHoursSpecification",
          "dayOfWeek": [
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
            "Sunday"
          ],
          "opens": "06:00",
          "closes": "22:00"
        }
      ],
      "sameAs": [
        "https://www.instagram.com/mariapaulaconfiteria/?hl=es",
        "https://www.facebook.com/profile.php?id=100048064763939",
        "https://wa.me/5491135433031"
      ]
    }
    </script>""",

    "menu/index.html": """    <!-- ═══════════════════════════════════════════ -->
    <!--  DATOS ESTRUCTURADOS SCHEMA.ORG (JSON-LD)   -->
    <!-- ═══════════════════════════════════════════ -->
    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": ["Bakery", "CafeOrCoffeeShop", "Restaurant"],
      "name": "María Paula Confitería",
      "image": "https://mariapaulaconfiteria.com/assets/images/logo-maria-paula-confiteria.png",
      "logo": "https://mariapaulaconfiteria.com/assets/images/logo-maria-paula-confiteria.png",
      "url": "https://mariapaulaconfiteria.com/menu/",
      "telephone": "+541146677707",
      "email": "1301mpaula@gmail.com",
      "hasMenu": "https://mariapaulaconfiteria.com/menu/",
      "priceRange": "$3.000 - $22.000 ARS",
      "currenciesAccepted": "ARS",
      "paymentAccepted": "Efectivo, Tarjeta de Débito, Tarjeta de Crédito, Mercado Pago",
      "servesCuisine": [
        "Pastelería Artesanal",
        "Cafetería de Especialidad",
        "Panadería",
        "Cocina Tradicional Argentina",
        "Heladería"
      ],
      "address": {
        "@type": "PostalAddress",
        "streetAddress": "Consejal Tribulato 1148",
        "addressLocality": "San Miguel",
        "addressRegion": "Buenos Aires",
        "postalCode": "B1663",
        "addressCountry": "AR"
      },
      "openingHoursSpecification": [
        {
          "@type": "OpeningHoursSpecification",
          "dayOfWeek": [
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
            "Sunday"
          ],
          "opens": "06:00",
          "closes": "22:00"
        }
      ],
      "sameAs": [
        "https://www.instagram.com/mariapaulaconfiteria/?hl=es",
        "https://www.facebook.com/profile.php?id=100048064763939",
        "https://wa.me/5491135433031"
      ]
    }
    </script>
    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": "Menu",
      "name": "Menú y Carta María Paula Confitería",
      "description": "Carta completa de cafetería de especialidad, pastelería artesanal, comidas, burgers, pastas caseras, pizzas y desayunos en San Miguel.",
      "url": "https://mariapaulaconfiteria.com/menu/",
      "inLanguage": "es-AR",
      "hasMenuSection": [
        {
          "@type": "MenuSection",
          "name": "Comidas",
          "description": "Burgers artesanales, pastas frescas caseras, pizzas, milanesas, grilladas y platos principales",
          "hasMenuItem": [
            {
              "@type": "MenuItem",
              "name": "Burger clásica",
              "description": "Hamburguesa artesanal con guarnición de papas fritas",
              "offers": {
                "@type": "Offer",
                "price": "16500",
                "priceCurrency": "ARS"
              }
            }
          ]
        },
        {
          "@type": "MenuSection",
          "name": "Desayunos y Meriendas",
          "description": "Combos con café de especialidad, tostados y medialunas de manteca artesanales",
          "hasMenuItem": [
            {
              "@type": "MenuItem",
              "name": "Desayuno Clásico",
              "description": "Café o té con 2 medialunas artesanales y jugo de naranja",
              "offers": {
                "@type": "Offer",
                "price": "6500",
                "priceCurrency": "ARS"
              }
            }
          ]
        },
        {
          "@type": "MenuSection",
          "name": "Pastelería",
          "description": "Tortas tradicionales y de autor, porciones dulces y masas finas de elaboración propia",
          "hasMenuItem": [
            {
              "@type": "MenuItem",
              "name": "Porción de Torta Artesanal",
              "description": "Variedades de tortas frescas elaboradas en nuestra confitería",
              "offers": {
                "@type": "Offer",
                "price": "7500",
                "priceCurrency": "ARS"
              }
            }
          ]
        },
        {
          "@type": "MenuSection",
          "name": "Bebidas",
          "description": "Café de especialidad en grano, bebidas calientes, infusiones, jugos y bebidas frías"
        }
      ]
    }
    </script>""",

    "catering/index.html": """    <!-- ═══════════════════════════════════════════ -->
    <!--  DATOS ESTRUCTURADOS SCHEMA.ORG (JSON-LD)   -->
    <!-- ═══════════════════════════════════════════ -->
    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": ["Bakery", "CafeOrCoffeeShop", "Restaurant"],
      "name": "María Paula Confitería",
      "image": "https://mariapaulaconfiteria.com/assets/images/logo-maria-paula-confiteria.png",
      "logo": "https://mariapaulaconfiteria.com/assets/images/logo-maria-paula-confiteria.png",
      "url": "https://mariapaulaconfiteria.com/catering/",
      "telephone": "+541146677707",
      "email": "1301mpaula@gmail.com",
      "priceRange": "$3.000 - $22.000 ARS",
      "currenciesAccepted": "ARS",
      "paymentAccepted": "Efectivo, Tarjeta de Débito, Tarjeta de Crédito, Mercado Pago",
      "address": {
        "@type": "PostalAddress",
        "streetAddress": "Consejal Tribulato 1148",
        "addressLocality": "San Miguel",
        "addressRegion": "Buenos Aires",
        "postalCode": "B1663",
        "addressCountry": "AR"
      },
      "openingHoursSpecification": [
        {
          "@type": "OpeningHoursSpecification",
          "dayOfWeek": [
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
            "Sunday"
          ],
          "opens": "06:00",
          "closes": "22:00"
        }
      ],
      "sameAs": [
        "https://www.instagram.com/mariapaulaconfiteria/?hl=es",
        "https://www.facebook.com/profile.php?id=100048064763939",
        "https://wa.me/5491135433031"
      ]
    }
    </script>
    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": "Service",
      "name": "Servicio de Catering Premium",
      "serviceType": "Catering y Eventos a Domicilio",
      "description": "Servicio integral de catering en salón y externo llave en mano para bodas, cumpleaños y eventos corporativos con carpas calefaccionadas, vajilla, mobiliario y gastronomía de excelencia.",
      "url": "https://mariapaulaconfiteria.com/catering/",
      "provider": {
        "@type": ["Bakery", "CafeOrCoffeeShop", "Restaurant"],
        "name": "María Paula Confitería",
        "url": "https://mariapaulaconfiteria.com/",
        "telephone": "+541146677707",
        "email": "1301mpaula@gmail.com"
      },
      "areaServed": {
        "@type": "AdministrativeArea",
        "name": "San Miguel y Zona Norte de Gran Buenos Aires"
      },
      "hasOfferCatalog": {
        "@type": "OfferCatalog",
        "name": "Propuestas de Catering María Paula",
        "itemListElement": [
          {
            "@type": "Offer",
            "itemOffered": {
              "@type": "Service",
              "name": "Catering en Salón",
              "description": "Celebración integral en los salones de María Paula con camareros, ambientación y menú artesanal."
            }
          },
          {
            "@type": "Offer",
            "itemOffered": {
              "@type": "Service",
              "name": "Catering Externo Llave en Mano",
              "description": "Servicio a domicilio en quintas y salones con armado de carpas, sonido, vajilla de gala y retiro posterior."
            }
          }
        ]
      },
      "potentialAction": {
        "@type": "CommunicateAction",
        "target": {
          "@type": "EntryPoint",
          "urlTemplate": "https://wa.me/5491135433031?text=Hola,%20escribo%20desde%20la%20web%20MariaPaulaConfiteria.com.%20Quisiera%20consultar%20disponibilidad%20y%20presupuesto%20para%20un%20servicio%20de%20Catering."
        }
      }
    }
    </script>""",

    "eventos/index.html": """    <!-- ═══════════════════════════════════════════ -->
    <!--  DATOS ESTRUCTURADOS SCHEMA.ORG (JSON-LD)   -->
    <!-- ═══════════════════════════════════════════ -->
    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": ["Bakery", "CafeOrCoffeeShop", "Restaurant"],
      "name": "María Paula Confitería",
      "image": "https://mariapaulaconfiteria.com/assets/images/logo-maria-paula-confiteria.png",
      "logo": "https://mariapaulaconfiteria.com/assets/images/logo-maria-paula-confiteria.png",
      "url": "https://mariapaulaconfiteria.com/eventos/",
      "telephone": "+541146677707",
      "email": "1301mpaula@gmail.com",
      "priceRange": "$3.000 - $22.000 ARS",
      "currenciesAccepted": "ARS",
      "paymentAccepted": "Efectivo, Tarjeta de Débito, Tarjeta de Crédito, Mercado Pago",
      "address": {
        "@type": "PostalAddress",
        "streetAddress": "Consejal Tribulato 1148",
        "addressLocality": "San Miguel",
        "addressRegion": "Buenos Aires",
        "postalCode": "B1663",
        "addressCountry": "AR"
      },
      "openingHoursSpecification": [
        {
          "@type": "OpeningHoursSpecification",
          "dayOfWeek": [
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
            "Sunday"
          ],
          "opens": "06:00",
          "closes": "22:00"
        }
      ],
      "sameAs": [
        "https://www.instagram.com/mariapaulaconfiteria/?hl=es",
        "https://www.facebook.com/profile.php?id=100048064763939",
        "https://wa.me/5491135433031"
      ]
    }
    </script>
    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": "EventVenue",
      "name": "Salones para Eventos Sociales y Corporativos – María Paula",
      "description": "Salones climatizados de arquitectura clásica en San Miguel para bodas, civiles, cumpleaños, coffee breaks y after office corporativos.",
      "url": "https://mariapaulaconfiteria.com/eventos/",
      "telephone": "+541146677707",
      "address": {
        "@type": "PostalAddress",
        "streetAddress": "Consejal Tribulato 1148",
        "addressLocality": "San Miguel",
        "addressRegion": "Buenos Aires",
        "postalCode": "B1663",
        "addressCountry": "AR"
      },
      "potentialAction": {
        "@type": "CommunicateAction",
        "target": {
          "@type": "EntryPoint",
          "urlTemplate": "https://wa.me/5491135433031?text=Hola,%20escribo%20desde%20la%20web%20MariaPaulaConfiteria.com.%20Quisiera%20solicitar%20un%20presupuesto%20para%20realizar%20un%20Evento."
        }
      }
    }
    </script>""",

    "regalos/index.html": """    <!-- ═══════════════════════════════════════════ -->
    <!--  DATOS ESTRUCTURADOS SCHEMA.ORG (JSON-LD)   -->
    <!-- ═══════════════════════════════════════════ -->
    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": ["Bakery", "CafeOrCoffeeShop", "Restaurant"],
      "name": "María Paula Confitería",
      "image": "https://mariapaulaconfiteria.com/assets/images/logo-maria-paula-confiteria.png",
      "logo": "https://mariapaulaconfiteria.com/assets/images/logo-maria-paula-confiteria.png",
      "url": "https://mariapaulaconfiteria.com/regalos/",
      "telephone": "+541146677707",
      "email": "1301mpaula@gmail.com",
      "priceRange": "$3.000 - $22.000 ARS",
      "currenciesAccepted": "ARS",
      "paymentAccepted": "Efectivo, Tarjeta de Débito, Tarjeta de Crédito, Mercado Pago",
      "address": {
        "@type": "PostalAddress",
        "streetAddress": "Consejal Tribulato 1148",
        "addressLocality": "San Miguel",
        "addressRegion": "Buenos Aires",
        "postalCode": "B1663",
        "addressCountry": "AR"
      },
      "openingHoursSpecification": [
        {
          "@type": "OpeningHoursSpecification",
          "dayOfWeek": [
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
            "Sunday"
          ],
          "opens": "06:00",
          "closes": "22:00"
        }
      ],
      "sameAs": [
        "https://www.instagram.com/mariapaulaconfiteria/?hl=es",
        "https://www.facebook.com/profile.php?id=100048064763939",
        "https://wa.me/5491135433031"
      ]
    }
    </script>
    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": "OfferCatalog",
      "name": "Gift Cards y Experiencias de Regalo María Paula",
      "url": "https://mariapaulaconfiteria.com/regalos/",
      "description": "Gift Cards de experiencias gastronómicas para regalar y disfrutar en las sucursales de María Paula Confitería.",
      "itemListElement": [
        {
          "@type": "Offer",
          "name": "Gift Card Experiencia Plata",
          "description": "Desayuno o merienda: café o té a elección, jugo de naranja, 2 medialunas o tostadas y porción de torta a elección.",
          "category": "GiftCard",
          "priceCurrency": "ARS",
          "url": "https://wa.me/5491135433031?text=Hola,%20escribo%20desde%20la%20web%20MariaPaulaConfiteria.com.%20Quisiera%20comprar%20una%20Gift%20Card%20PLATA"
        },
        {
          "@type": "Offer",
          "name": "Gift Card Experiencia Oro",
          "description": "Brunch o almuerzo ligero: plato principal de carta, bebida sin alcohol, postre o café y servicio de mesa.",
          "category": "GiftCard",
          "priceCurrency": "ARS",
          "url": "https://wa.me/5491135433031?text=Hola,%20escribo%20desde%20la%20web%20MariaPaulaConfiteria.com.%20Quisiera%20comprar%20una%20Gift%20Card%20ORO"
        },
        {
          "@type": "Offer",
          "name": "Gift Card Experiencia Platino",
          "description": "Cena completa: entrada para compartir, 2 platos principales, vino a elección de la casa, 2 postres y café.",
          "category": "GiftCard",
          "priceCurrency": "ARS",
          "url": "https://wa.me/5491135433031?text=Hola,%20escribo%20desde%20la%20web%20MariaPaulaConfiteria.com.%20Quisiera%20comprar%20una%20Gift%20Card%20PLATINO"
        }
      ]
    }
    </script>""",

    "contacto/index.html": """    <!-- ═══════════════════════════════════════════ -->
    <!--  DATOS ESTRUCTURADOS SCHEMA.ORG (JSON-LD)   -->
    <!-- ═══════════════════════════════════════════ -->
    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": "ContactPage",
      "name": "Contacto | María Paula Confitería",
      "description": "Información de contacto, mapa de ubicación, teléfonos y horarios de atención de las sucursales de María Paula Confitería en San Miguel.",
      "url": "https://mariapaulaconfiteria.com/contacto/",
      "mainEntity": {
        "@type": ["Bakery", "CafeOrCoffeeShop", "Restaurant"],
        "name": "María Paula Confitería",
        "url": "https://mariapaulaconfiteria.com/",
        "logo": "https://mariapaulaconfiteria.com/assets/images/logo-maria-paula-confiteria.png",
        "image": "https://mariapaulaconfiteria.com/assets/images/logo-maria-paula-confiteria.png",
        "email": "1301mpaula@gmail.com",
        "telephone": "+541146677707",
        "priceRange": "$3.000 - $22.000 ARS",
        "currenciesAccepted": "ARS",
        "paymentAccepted": "Efectivo, Tarjeta de Débito, Tarjeta de Crédito, Mercado Pago",
        "hasMap": "https://www.google.com/maps/d/embed?mid=1fSXvjay35u7iqkkcqWaBSTBF6aM7nZc",
        "contactPoint": [
          {
            "@type": "ContactPoint",
            "telephone": "+541146677707",
            "contactType": "Sucursal Tribulato - Atención y Reservas",
            "areaServed": "AR",
            "availableLanguage": "Spanish"
          },
          {
            "@type": "ContactPoint",
            "telephone": "+541144518282",
            "contactType": "Sucursal Balbín - Atención y Reservas",
            "areaServed": "AR",
            "availableLanguage": "Spanish"
          },
          {
            "@type": "ContactPoint",
            "telephone": "+5491135433031",
            "contactType": "WhatsApp Atención y Eventos",
            "areaServed": "AR",
            "availableLanguage": "Spanish"
          }
        ],
        "department": [
          {
            "@type": ["Bakery", "CafeOrCoffeeShop", "Restaurant"],
            "name": "María Paula Confitería – Sucursal Tribulato",
            "telephone": "+541146677707",
            "url": "https://mariapaulaconfiteria.com/sucursal-tribulato/",
            "address": {
              "@type": "PostalAddress",
              "streetAddress": "Consejal Tribulato 1148",
              "addressLocality": "San Miguel",
              "addressRegion": "Buenos Aires",
              "postalCode": "B1663",
              "addressCountry": "AR"
            },
            "openingHoursSpecification": [
              {
                "@type": "OpeningHoursSpecification",
                "dayOfWeek": [
                  "Monday",
                  "Tuesday",
                  "Wednesday",
                  "Thursday",
                  "Friday",
                  "Saturday",
                  "Sunday"
                ],
                "opens": "06:00",
                "closes": "22:00"
              }
            ]
          },
          {
            "@type": ["Bakery", "CafeOrCoffeeShop", "Restaurant"],
            "name": "María Paula Confitería – Sucursal Balbín",
            "telephone": "+541144518282",
            "url": "https://mariapaulaconfiteria.com/sucursal-balbin/",
            "address": {
              "@type": "PostalAddress",
              "streetAddress": "Av. Dr. Ricardo Balbín 1301",
              "addressLocality": "San Miguel",
              "addressRegion": "Buenos Aires",
              "postalCode": "B1663",
              "addressCountry": "AR"
            },
            "openingHoursSpecification": [
              {
                "@type": "OpeningHoursSpecification",
                "dayOfWeek": [
                  "Monday",
                  "Tuesday",
                  "Wednesday",
                  "Thursday",
                  "Friday",
                  "Saturday",
                  "Sunday"
                ],
                "opens": "06:00",
                "closes": "22:00"
              }
            ]
          }
        ]
      }
    }
    </script>""",

    "nuestra-cocina/index.html": """    <!-- ═══════════════════════════════════════════ -->
    <!--  DATOS ESTRUCTURADOS SCHEMA.ORG (JSON-LD)   -->
    <!-- ═══════════════════════════════════════════ -->
    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": ["Bakery", "CafeOrCoffeeShop", "Restaurant"],
      "name": "María Paula Confitería – Nuestra Cocina",
      "image": "https://mariapaulaconfiteria.com/assets/images/panaderia-medialunas-artesanales-cafeteria-desktop.webp",
      "logo": "https://mariapaulaconfiteria.com/assets/images/logo-maria-paula-confiteria.png",
      "url": "https://mariapaulaconfiteria.com/nuestra-cocina/",
      "telephone": "+541146677707",
      "email": "1301mpaula@gmail.com",
      "hasMenu": "https://mariapaulaconfiteria.com/menu/",
      "priceRange": "$3.000 - $22.000 ARS",
      "currenciesAccepted": "ARS",
      "paymentAccepted": "Efectivo, Tarjeta de Débito, Tarjeta de Crédito, Mercado Pago",
      "servesCuisine": [
        "Pastelería Artesanal",
        "Cafetería de Especialidad",
        "Panadería de Masa Madre",
        "Platos de Autor Tradicionales"
      ],
      "address": {
        "@type": "PostalAddress",
        "streetAddress": "Consejal Tribulato 1148",
        "addressLocality": "San Miguel",
        "addressRegion": "Buenos Aires",
        "postalCode": "B1663",
        "addressCountry": "AR"
      },
      "openingHoursSpecification": [
        {
          "@type": "OpeningHoursSpecification",
          "dayOfWeek": [
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
            "Sunday"
          ],
          "opens": "06:00",
          "closes": "22:00"
        }
      ],
      "sameAs": [
        "https://www.instagram.com/mariapaulaconfiteria/?hl=es",
        "https://www.facebook.com/profile.php?id=100048064763939",
        "https://wa.me/5491135433031"
      ]
    }
    </script>
    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": "VideoObject",
      "name": "Nuestra Cocina y Taller Artesanal - María Paula Confitería",
      "description": "Descubra el proceso artesanal de elaboración de panadería, medialunas y cafetería de especialidad en María Paula.",
      "thumbnailUrl": "https://mariapaulaconfiteria.com/assets/images/video-hero-poster.webp",
      "uploadDate": "2024-01-15T08:00:00-03:00",
      "contentUrl": "https://mariapaulaconfiteria.com/assets/videos/hero-loop.mp4",
      "embedUrl": "https://mariapaulaconfiteria.com/assets/videos/hero-loop.mp4"
    }
    </script>"""
}

def validate_schemas():
    for rel_path, replacement in SCHEMAS.items():
        scripts = re.findall(r'<script type="application/ld\+json">(.*?)</script>', replacement, flags=re.DOTALL)
        for i, s in enumerate(scripts):
            try:
                data = json.loads(s.strip())
                assert "@context" in data
                assert "@type" in data
            except Exception as e:
                print(f"Error validating JSON in {rel_path} (script {i}): {e}")
                return False
    print("All replacement JSON-LD blocks are 100% syntactically valid JSON!")
    return True

def apply_schemas():
    if not validate_schemas():
        return
    
    pattern = re.compile(
        r'([ \t]*<!-- ═+ -->\s*<!--  DATOS ESTRUCTURADOS SCHEMA\.ORG \(JSON-LD\)   -->\s*<!-- ═+ -->\s*(?:<script type="application/ld\+json">.*?</script>\s*)+)(?=[ \t]*<!-- Main Project Styles -->)',
        re.DOTALL
    )

    for rel_path, replacement in SCHEMAS.items():
        full_path = os.path.join(BASE_DIR, rel_path)
        with open(full_path, "r", encoding="utf-8") as f:
            content = f.read()

        match = pattern.search(content)
        if not match:
            print(f"Pattern match FAILED for {rel_path}")
            continue

        new_content = content[:match.start()] + replacement + "\n\n" + content[match.end():]
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"Updated {rel_path} successfully!")

if __name__ == "__main__":
    apply_schemas()
