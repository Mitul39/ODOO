import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card'
import { Users, Target, Heart, Lightbulb, Globe, Award } from 'lucide-react'

const AboutUs = () => {
  const values = [
    {
      icon: <Users className="h-8 w-8 text-primary" />,
      title: "Community First",
      description: "We believe in the power of community-driven learning and mutual support."
    },
    {
      icon: <Target className="h-8 w-8 text-primary" />,
      title: "Goal-Oriented",
      description: "Every interaction is designed to help you achieve your learning objectives."
    },
    {
      icon: <Heart className="h-8 w-8 text-primary" />,
      title: "Passion-Driven",
      description: "We connect people who are passionate about sharing and learning."
    },
    {
      icon: <Lightbulb className="h-8 w-8 text-primary" />,
      title: "Innovation",
      description: "Constantly improving the way people learn and teach skills."
    },
    {
      icon: <Globe className="h-8 w-8 text-primary" />,
      title: "Global Reach",
      description: "Connecting learners and teachers from around the world."
    },
    {
      icon: <Award className="h-8 w-8 text-primary" />,
      title: "Excellence",
      description: "Committed to providing the highest quality learning experiences."
    }
  ]

  return (
    <div className="min-h-screen py-12 px-4">
      <div className="container mx-auto max-w-6xl">
        {/* Hero Section */}
        <div className="text-center mb-16">
          <div className="skill-swap-gradient w-16 h-16 rounded-2xl flex items-center justify-center mx-auto mb-8">
            <span className="text-white font-bold text-2xl">S</span>
          </div>
          <h1 className="text-4xl md:text-5xl font-bold mb-6">About SkillSwap</h1>
          <p className="text-xl text-muted-foreground max-w-3xl mx-auto leading-relaxed">
            As students, we have looked for upskilling everywhere. Mostly, we end up paying big amounts to gain 
            certifications and learn relevant skills. We thought of SkillSwap to resolve that. Learning new skills and 
            gaining more knowledge all while networking with talented people!
          </p>
        </div>

        {/* Mission Section */}
        <div className="mb-16">
          <Card className="bg-gradient-to-br from-primary/5 to-accent/5 border-primary/20">
            <CardHeader className="text-center">
              <CardTitle className="text-2xl md:text-3xl mb-4">Our Mission</CardTitle>
            </CardHeader>
            <CardContent className="text-center">
              <p className="text-lg text-muted-foreground max-w-4xl mx-auto leading-relaxed">
                At SkillSwap, we believe in the power of learning and sharing knowledge. Our platform connects 
                individuals from diverse backgrounds to exchange practical skills and expertise. Whether you're a 
                seasoned professional looking to mentor others or a beginner eager to learn, SkillSwap provides a 
                supportive environment for growth and collaboration.
              </p>
            </CardContent>
          </Card>
        </div>

        {/* Vision Section */}
        <div className="mb-16">
          <Card>
            <CardHeader className="text-center">
              <CardTitle className="text-2xl md:text-3xl mb-4">Our Vision</CardTitle>
            </CardHeader>
            <CardContent className="text-center">
              <p className="text-lg text-muted-foreground max-w-4xl mx-auto leading-relaxed">
                Our mission is to empower individuals to unlock their full potential through skill sharing. By facilitating 
                meaningful interactions and fostering a culture of lifelong learning, we aim to create a community where 
                everyone has the opportunity to thrive.
              </p>
            </CardContent>
          </Card>
        </div>

        {/* Values Section */}
        <div className="mb-16">
          <div className="text-center mb-12">
            <h2 className="text-3xl md:text-4xl font-bold mb-4">Our Values</h2>
            <p className="text-xl text-muted-foreground">
              The principles that guide everything we do
            </p>
          </div>
          
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            {values.map((value, index) => (
              <Card key={index} className="text-center hover:shadow-lg transition-shadow">
                <CardHeader>
                  <div className="flex justify-center mb-4">
                    {value.icon}
                  </div>
                  <CardTitle className="text-xl">{value.title}</CardTitle>
                </CardHeader>
                <CardContent>
                  <CardDescription className="text-base">
                    {value.description}
                  </CardDescription>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>

        {/* Story Section */}
        <div className="mb-16">
          <Card className="bg-muted/30">
            <CardHeader className="text-center">
              <CardTitle className="text-2xl md:text-3xl mb-4">Our Story</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="max-w-4xl mx-auto space-y-6 text-lg text-muted-foreground leading-relaxed">
                <p>
                  SkillSwap was born from a simple observation: traditional learning can be expensive, impersonal, 
                  and often disconnected from real-world application. As students ourselves, we experienced the 
                  frustration of paying high fees for courses that didn't always deliver practical value.
                </p>
                <p>
                  We realized that some of the most valuable learning happens through peer-to-peer interaction. 
                  The developer who learned design from a colleague, the marketer who taught coding to a friend, 
                  the chef who shared culinary secrets with a neighbor – these exchanges create lasting knowledge 
                  and meaningful connections.
                </p>
                <p>
                  Today, SkillSwap is more than just a platform – it's a movement toward democratizing education 
                  and making skill development accessible to everyone. We're building a world where knowledge 
                  flows freely, where teaching and learning happen naturally, and where every person has the 
                  opportunity to both share their expertise and discover new passions.
                </p>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Team Section */}
        <div className="text-center">
          <h2 className="text-3xl md:text-4xl font-bold mb-6">Join Our Community</h2>
          <p className="text-xl text-muted-foreground mb-8 max-w-3xl mx-auto">
            We're always looking for passionate individuals who believe in the power of shared learning. 
            Whether you're a teacher, learner, or both, there's a place for you in the SkillSwap community.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <a 
              href="/register" 
              className="inline-flex items-center justify-center rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 bg-primary text-primary-foreground hover:bg-primary/90 h-10 px-4 py-2"
            >
              Start Your Journey
            </a>
            <a 
              href="/why-skillswap" 
              className="inline-flex items-center justify-center rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 border border-input bg-background hover:bg-accent hover:text-accent-foreground h-10 px-4 py-2"
            >
              Learn More
            </a>
          </div>
        </div>
      </div>
    </div>
  )
}

export default AboutUs

