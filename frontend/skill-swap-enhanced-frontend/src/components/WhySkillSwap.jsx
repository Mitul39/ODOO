import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card'
import { Badge } from './ui/badge'
import { GraduationCap, Share2, Users, Lightbulb, TrendingUp, Globe, CheckCircle } from 'lucide-react'

const WhySkillSwap = () => {
  const benefits = [
    {
      icon: <GraduationCap className="h-12 w-12 text-primary" />,
      title: "Learn From Experts",
      description: "Gain insights and practical knowledge directly from experienced mentors who excel in their respective fields. Whether it's mastering a new programming language, honing your culinary skills, or delving into the world of digital marketing, our mentors are here to guide you every step of the way.",
      highlight: "Direct mentorship"
    },
    {
      icon: <Share2 className="h-12 w-12 text-primary" />,
      title: "Share Your Expertise",
      description: "Have a skill or passion you're eager to share? SkillSwap provides a platform for you to become a mentor yourself. Share your expertise with others, foster a sense of community, and contribute to the growth of aspiring learners.",
      highlight: "Become a mentor"
    },
    {
      icon: <Users className="h-12 w-12 text-primary" />,
      title: "Collaborative Environment",
      description: "Our community thrives on collaboration. Connect with like-minded individuals, participate in group projects, and engage in discussions that fuel creativity and innovation. SkillSwap isn't just about individual growth—it's about collective advancement.",
      highlight: "Community driven"
    },
    {
      icon: <TrendingUp className="h-12 w-12 text-primary" />,
      title: "Diverse Learning Opportunities",
      description: "From technical skills to creative arts, from business acumen to personal development, SkillSwap offers a wide range of learning opportunities. Explore new domains, discover hidden talents, and expand your horizons in ways you never thought possible.",
      highlight: "Endless possibilities"
    }
  ]

  const features = [
    "Free skill exchange platform",
    "Verified mentor profiles", 
    "Flexible scheduling system",
    "Achievement badges and recognition",
    "Global community access",
    "Personalized skill recommendations",
    "Session recording capabilities",
    "Progress tracking tools"
  ]

  const stats = [
    { number: "10,000+", label: "Active Users" },
    { number: "500+", label: "Skills Available" },
    { number: "25,000+", label: "Sessions Completed" },
    { number: "95%", label: "Satisfaction Rate" }
  ]

  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="py-20 px-4 bg-gradient-to-br from-primary/10 to-accent/10">
        <div className="container mx-auto max-w-4xl text-center">
          <h1 className="text-4xl md:text-5xl font-bold mb-6">
            Why Choose SkillSwap?
          </h1>
          <p className="text-xl text-muted-foreground mb-8 max-w-3xl mx-auto leading-relaxed">
            At Skill Swap, we believe in the power of mutual learning and collaboration. Here's why Skill Swap is the 
            ultimate platform for skill acquisition and knowledge exchange:
          </p>
        </div>
      </section>

      {/* Benefits Section */}
      <section className="py-20 px-4">
        <div className="container mx-auto max-w-6xl">
          <div className="space-y-16">
            {benefits.map((benefit, index) => (
              <div key={index} className={`flex flex-col ${index % 2 === 0 ? 'lg:flex-row' : 'lg:flex-row-reverse'} items-center gap-12`}>
                <div className="flex-1">
                  <Card className="h-full border-primary/20 hover:shadow-lg transition-shadow">
                    <CardHeader>
                      <div className="flex items-center gap-4 mb-4">
                        {benefit.icon}
                        <div>
                          <Badge variant="secondary" className="mb-2">
                            {benefit.highlight}
                          </Badge>
                          <CardTitle className="text-2xl">{benefit.title}</CardTitle>
                        </div>
                      </div>
                    </CardHeader>
                    <CardContent>
                      <CardDescription className="text-base leading-relaxed">
                        {benefit.description}
                      </CardDescription>
                    </CardContent>
                  </Card>
                </div>
                <div className="flex-1 flex justify-center">
                  <div className="w-64 h-64 bg-gradient-to-br from-primary/20 to-accent/20 rounded-2xl flex items-center justify-center">
                    <div className="text-6xl opacity-20">
                      {benefit.icon}
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="py-20 px-4 bg-muted/30">
        <div className="container mx-auto max-w-6xl">
          <div className="text-center mb-12">
            <h2 className="text-3xl md:text-4xl font-bold mb-4">Our Impact</h2>
            <p className="text-xl text-muted-foreground">
              Numbers that speak to our community's success
            </p>
          </div>
          
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
            {stats.map((stat, index) => (
              <div key={index} className="text-center">
                <div className="text-3xl md:text-4xl font-bold text-primary mb-2">
                  {stat.number}
                </div>
                <div className="text-muted-foreground font-medium">
                  {stat.label}
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 px-4">
        <div className="container mx-auto max-w-4xl">
          <div className="text-center mb-12">
            <h2 className="text-3xl md:text-4xl font-bold mb-4">Platform Features</h2>
            <p className="text-xl text-muted-foreground">
              Everything you need for successful skill exchange
            </p>
          </div>
          
          <div className="grid md:grid-cols-2 gap-6">
            {features.map((feature, index) => (
              <div key={index} className="flex items-center gap-3 p-4 rounded-lg bg-card border">
                <CheckCircle className="h-5 w-5 text-primary flex-shrink-0" />
                <span className="text-base">{feature}</span>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 px-4 bg-gradient-to-r from-primary to-accent">
        <div className="container mx-auto max-w-4xl text-center">
          <h2 className="text-3xl md:text-4xl font-bold text-white mb-6">
            Ready to Transform Your Learning Journey?
          </h2>
          <p className="text-xl text-white/90 mb-8 max-w-2xl mx-auto">
            Join thousands of learners and mentors who are already experiencing the power of skill exchange. 
            Your next breakthrough is just one connection away.
          </p>
          
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <a 
              href="/register" 
              className="inline-flex items-center justify-center rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 bg-white text-primary hover:bg-white/90 h-11 px-8"
            >
              Start Learning Today
            </a>
            <a 
              href="/about" 
              className="inline-flex items-center justify-center rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 border border-white text-white hover:bg-white hover:text-primary h-11 px-8"
            >
              Learn More About Us
            </a>
          </div>
        </div>
      </section>
    </div>
  )
}

export default WhySkillSwap

