import { Link } from 'react-router-dom'
import { useAuth } from '../hooks/useAuth'
import { Button } from './ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card'
import { Badge } from './ui/badge'
import { ArrowRight, Users, BookOpen, Trophy, Star, CheckCircle } from 'lucide-react'

const Homepage = () => {
  const { isAuthenticated } = useAuth()

  const features = [
    {
      icon: <Users className="h-8 w-8 text-primary" />,
      title: "Connect with Experts",
      description: "Find skilled professionals ready to share their knowledge and learn from you."
    },
    {
      icon: <BookOpen className="h-8 w-8 text-primary" />,
      title: "Learn New Skills",
      description: "Discover new abilities through hands-on sessions with experienced mentors."
    },
    {
      icon: <Trophy className="h-8 w-8 text-primary" />,
      title: "Earn Badges",
      description: "Build your reputation and unlock achievements as you teach and learn."
    }
  ]

  const steps = [
    {
      number: "01",
      title: "Create Your Profile",
      description: "Tell us about your skills and what you want to learn"
    },
    {
      number: "02", 
      title: "Find Your Match",
      description: "Browse users and find the perfect skill exchange partner"
    },
    {
      number: "03",
      title: "Start Learning",
      description: "Schedule sessions and begin your skill exchange journey"
    }
  ]

  const testimonials = [
    {
      name: "Sarah Chen",
      role: "UX Designer",
      content: "SkillSwap helped me learn Python while teaching design. Amazing community!",
      rating: 5,
      badge: "Gold"
    },
    {
      name: "Mike Rodriguez", 
      role: "Software Engineer",
      content: "I've improved my presentation skills and taught 20+ coding sessions.",
      rating: 5,
      badge: "Platinum"
    },
    {
      name: "Emma Thompson",
      role: "Marketing Manager", 
      content: "The badge system keeps me motivated. Already earned my Silver badge!",
      rating: 5,
      badge: "Silver"
    }
  ]

  const getBadgeColor = (badgeLevel) => {
    switch (badgeLevel) {
      case 'Bronze': return 'bg-amber-600'
      case 'Silver': return 'bg-gray-400'
      case 'Gold': return 'bg-yellow-500'
      case 'Platinum': return 'bg-purple-600'
      default: return 'bg-gray-500'
    }
  }

  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="relative py-20 px-4 text-center bg-gradient-to-br from-primary/10 to-accent/10">
        <div className="container mx-auto max-w-4xl">
          <div className="bg-gradient-to-r from-primary to-accent w-20 h-20 rounded-2xl flex items-center justify-center mx-auto mb-8">
            <span className="text-white font-bold text-3xl">S</span>
          </div>
          
          <h1 className="text-5xl md:text-6xl font-bold mb-6 bg-gradient-to-r from-primary to-accent bg-clip-text text-transparent">
            Exchange Skills,<br />Grow Together
          </h1>
          
          <p className="text-xl text-muted-foreground mb-8 max-w-2xl mx-auto">
            Join a community where learning meets teaching. Share your expertise, 
            discover new skills, and build meaningful connections through skill exchange.
          </p>
          
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            {isAuthenticated ? (
              <>
                <Button size="lg" asChild>
                  <Link to="/browse">
                    Browse Users <ArrowRight className="ml-2 h-5 w-5" />
                  </Link>
                </Button>
                <Button size="lg" variant="outline" asChild>
                  <Link to="/dashboard">Go to Dashboard</Link>
                </Button>
              </>
            ) : (
              <>
                <Button size="lg" asChild>
                  <Link to="/register">
                    Get Started <ArrowRight className="ml-2 h-5 w-5" />
                  </Link>
                </Button>
                <Button size="lg" variant="outline" asChild>
                  <Link to="/login">Sign In</Link>
                </Button>
              </>
            )}
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 px-4">
        <div className="container mx-auto max-w-6xl">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold mb-4">Why Choose SkillSwap?</h2>
            <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
              Experience the power of peer-to-peer learning in a supportive community
            </p>
          </div>
          
          <div className="grid md:grid-cols-3 gap-8">
            {features.map((feature, index) => (
              <Card key={index} className="text-center hover:shadow-lg transition-shadow">
                <CardHeader>
                  <div className="flex justify-center mb-4">
                    {feature.icon}
                  </div>
                  <CardTitle className="text-xl">{feature.title}</CardTitle>
                </CardHeader>
                <CardContent>
                  <CardDescription className="text-base">
                    {feature.description}
                  </CardDescription>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* How It Works Section */}
      <section className="py-20 px-4 bg-muted/30">
        <div className="container mx-auto max-w-6xl">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold mb-4">How It Works</h2>
            <p className="text-xl text-muted-foreground">
              Start your skill exchange journey in three simple steps
            </p>
          </div>
          
          <div className="grid md:grid-cols-3 gap-8">
            {steps.map((step, index) => (
              <div key={index} className="text-center">
                <div className="bg-gradient-to-r from-primary to-accent w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-6">
                  <span className="text-white font-bold text-xl">{step.number}</span>
                </div>
                <h3 className="text-xl font-semibold mb-4">{step.title}</h3>
                <p className="text-muted-foreground">{step.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Testimonials Section */}
      <section className="py-20 px-4">
        <div className="container mx-auto max-w-6xl">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold mb-4">What Our Community Says</h2>
            <p className="text-xl text-muted-foreground">
              Real stories from real skill swappers
            </p>
          </div>
          
          <div className="grid md:grid-cols-3 gap-8">
            {testimonials.map((testimonial, index) => (
              <Card key={index} className="hover:shadow-lg transition-shadow">
                <CardHeader>
                  <div className="flex items-center justify-between mb-2">
                    <div>
                      <CardTitle className="text-lg">{testimonial.name}</CardTitle>
                      <CardDescription>{testimonial.role}</CardDescription>
                    </div>
                    <Badge className={getBadgeColor(testimonial.badge)}>
                      {testimonial.badge}
                    </Badge>
                  </div>
                  <div className="flex items-center">
                    {[...Array(testimonial.rating)].map((_, i) => (
                      <Star key={i} className="h-4 w-4 fill-yellow-400 text-yellow-400" />
                    ))}
                  </div>
                </CardHeader>
                <CardContent>
                  <p className="text-muted-foreground">"{testimonial.content}"</p>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 px-4 bg-gradient-to-r from-primary to-accent">
        <div className="container mx-auto max-w-4xl text-center">
          <h2 className="text-3xl md:text-4xl font-bold text-white mb-6">
            Ready to Start Your Skill Exchange Journey?
          </h2>
          <p className="text-xl text-white/90 mb-8 max-w-2xl mx-auto">
            Join thousands of learners and teachers in our growing community. 
            Your next skill is just a swap away.
          </p>
          
          {!isAuthenticated && (
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Button size="lg" variant="secondary" asChild>
                <Link to="/register">
                  Join SkillSwap Today <ArrowRight className="ml-2 h-5 w-5" />
                </Link>
              </Button>
              <Button size="lg" variant="outline" className="text-white border-white hover:bg-white hover:text-primary" asChild>
                <Link to="/about">Learn More</Link>
              </Button>
            </div>
          )}
        </div>
      </section>
    </div>
  )
}

export default Homepage

