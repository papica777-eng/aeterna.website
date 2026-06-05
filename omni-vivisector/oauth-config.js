// Aeterna Labs OAuth Config - Zero Hardcoding
const OAUTH_CONFIG = {
    google: {
        clientId: "101327948-googleclientid.apps.googleusercontent.com", // Replace with your Google Client ID
        authUrl: "https://accounts.google.com/o/oauth2/v2/auth",
        scope: "https://www.googleapis.com/auth/userinfo.email https://www.googleapis.com/auth/userinfo.profile",
        responseType: "token"
    },
    github: {
        clientId: "ov_git_101327948", // Replace with your GitHub Client ID
        authUrl: "https://github.com/login/oauth/authorize",
        scope: "user:email",
        responseType: "code"
    }
};
