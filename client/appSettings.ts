export const AppSettings = {
    SERVER : (process.env.NODE_ENV == 'production')
        ? 'https://arctic.DOMAIN/licenses'
        : 'http://localhost:8000/',
}
