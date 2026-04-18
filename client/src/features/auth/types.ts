// Register types
export type RegisterPayload = {
  email: string;
  password: string;
  full_name: string;
};

export type RegisterData = {
  user_id: string;
  access_token: string;
};

// Login types
export type LoginPayload = {
  email: string;
  password: string;
};

export type LoginData = {
  user_id: string;
  access_token: string;
};

// User type
export type UserData = {
  user_id: string;
  email: string;
  full_name?: string;
}