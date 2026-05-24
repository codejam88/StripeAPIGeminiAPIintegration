# StripeAPIGeminiAPIintegration
A backend microservice that bridges a secure payment gateway with advanced generative AI.
Paid AI Generation Microservice
A backend microservice that bridges a secure payment gateway with advanced generative AI. The application processes user-submitted prompts via a custom front-end interface, handles automated monetization verification using event-driven architecture, and securely triggers an enterprise large language model (LLM) to generate ultra-concise, context-aware content.

🛠️ Core Skills & Architecture Breakdown
Asynchronous Web Frameworks (FastAPI / Uvicorn): Developed structured, high-performance, asynchronous REST API endpoints to manage front-end presentation layer requests and high-traffic event queues.

Event-Driven Integration (Stripe Webhooks & CLI): Implemented cryptographic webhook signature verification (stripe.Webhook.construct_event) to securely process transactional event streams. Utilized the Stripe CLI to orchestrate a secure, local-to-cloud tunnel forwarding real-time webhook payload events (checkout.session.completed).

State & Metadata Management: Engineered custom bracket-lookup parsing structures to securely embed user state (user_prompt) directly within third-party transactional metadata payloads, safeguarding transient runtime data during cross-platform redirection loops.

Enterprise LLM Integration (Google GenAI SDK): Implemented the standard google-genai client client infrastructure. Leveraged gemini-2.5-flash with optimized string prompt engineering to govern output metrics, restricting structural formatting strictly to a 3-line 5-7-5 syllable Haiku schema.

Environment Security & Configuration: Isolated production credentials (API tokens, cryptographic signing secrets, network port values) out of runtime source code utilizing python-dotenv environment injection frameworks.

💻 Technology Stack
Languages: Python 3.10+, HTML5, CSS3

Frameworks: FastAPI, Uvicorn, Starlette

APIs & SDKs: Google GenAI SDK (gemini-2.5-flash), Stripe Developer SDK

DevOps & Security: Stripe CLI, Linux Terminal Environment, Dotenv (.env)


The system operates on an event-driven architecture that ensures content is only generated after transactional validation.

Plaintext
[ User Prompt ] ---> ( FastAPI Backend ) ---> Generates Stripe Hosted Checkout Url
                           |
                           v
                     [ User Pays $1 ]
                           |
                           v
[ Stripe Servers ] ---> ( Stripe CLI Tunnel ) ---> [ POST /webhook ]
                                                         | (Verifies Signature)
                                                         v
                                                 [ Extracts Metadata ]
                                                         |
                                                         v
[ Terminal Console ] <--- [ Return Haiku ] <--- ( Gemini 2.5 Flash API )
Initiation: The user inputs a prompt into the frontend and hits submit. The FastAPI backend receives the string and attaches it to a newly generated Stripe Checkout Session within the immutable metadata property.

Monetization: The user is redirected to a secure, Stripe-hosted payment page.

Asynchronous Verification: Upon a successful charge, Stripe emits a checkout.session.completed event. The local Stripe CLI daemon intercepts this payload and securely forwards it to the backend's /webhook endpoint.


****AT THE END OF THE PURCHASE, GEMINI WILL WRITE A SMALL HAIKU ABOUT YOUR PURCHASE.****
Validation & Extraction: The backend cryptographically verifies the webhook signature. It then securely extracts the original user prompt directly out of the transactional metadata.

LLM Orchestration: The backend passes the recovered prompt to the Google GenAI SDK using structural parameters that force the gemini-2.5-flash model to return a strict 5-7-5 syllable Haiku, printing the final output cleanly to the terminal.
