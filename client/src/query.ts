/*

FIXME: I would like to code these directly as .graphql files
but I don't know how to do that yet.

See https://parceljs.org/languages/graphql/

*/
import { gql } from '@apollo/client'

export const GET_LICENSES = gql`
    query GetLicenses() {
        licenses() {
            id
            product
            user
            checkout
        }
    }
`;

export const PING = gql`
    query Ping {
        timestamp
    }
`;
