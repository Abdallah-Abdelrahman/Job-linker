export type Job = {
  id: string;
  application_deadline: Date | null;
  exper_years: string;
  is_open: boolean;
  job_description: string;
  job_title: string;
  location: string;
  major: string;
  salary: number;
  skills: string[];
  responsibilities: string[];
};

export type Recruiter = {
  jobs: Job[];
};

export type ContactInfo = {
  company_address: string;
  company_email: string;
  company_name: string;
};

export type Data = {
  bio: string | null;
  contact_info: ContactInfo;
  email: string;
  image_url: string | null;
  name: string;
  recruiter: Recruiter;
};

export type Experience = {
  title: string;
  company: string;
  start_date: Date;
  end_date: Date;
  description: string;
};
export type Application = {
  title: string;
  company: string;
  start_date: Date;
  end_date: Date;
  description: string;
};
export type Skill = {
  id: string;
  name: string;
};
export type Contact = {
  address: string;
  linkded: string;
  github: string;
  phone: string;
  whatsapp: string;
};
export type Language = { id: string; name: string };

type Education = {
  degree: string;
  institute: string;
  start_date: Date;
  end_date: Date;
  description: string;
};
export type CandData = {
  name: string;
  email: string;
  image_url: string;
  contact_info: Contact;
  bio: string;
  candidate: {
    major: { name: string };
    skills: Skill[];
    languages: Language[];
    applications: Application[];
    experiences: Experience[];
    education: Education[];
  };
};
export interface CandidateProp {
  data?: CandData;
  as?: 'recruiter';
}

export interface RecruiterProp {
  data: Data;
}
