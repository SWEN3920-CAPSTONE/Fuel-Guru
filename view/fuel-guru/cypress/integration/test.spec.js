// https://docs.cypress.io/api/introduction/api.html

describe('Visiting the Home Page', () => {
  it('visits the app root url', () => {
    cy.visit('http://localhost:3000/')
    cy.contains('h1', 'Welcome to Fuel Guru')
    cy.get('#home-img')
  })
})

describe('ET1', () => {
  it('Creates a Fuel Guru account', () => {
    cy.visit('http://localhost:3000/signup')
    
  }),
  it('Creates a Fuel Guru account', () => {
    cy.visit('http://localhost:3000/signup')
    
  })
})