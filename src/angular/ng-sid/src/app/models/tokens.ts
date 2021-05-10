export class Tokens {
    access: string;
    refresh: string;
  }

  export class DecodedToken {
    name: string;
    exp: number;
    photo: string;
    user_id: number;
    jti: string;
    token_type: string;
  }